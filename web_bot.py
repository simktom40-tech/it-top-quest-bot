import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

from bot import build_app

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = os.environ["BASE_URL"].rstrip("/")
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
telegram_app = build_app(TOKEN)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(
        url=f"{BASE_URL}/webhook/{WEBHOOK_SECRET}",
        allowed_updates=["message"],
    )
    yield
    await telegram_app.bot.delete_webhook()
    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(title="IT Top Quest Bot", lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "ok", "service": "it-top-quest-bot"}


@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=404)
    from telegram import Update
    update = Update.de_json(await request.json(), telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return {"ok": True}
