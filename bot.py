import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from quest import QUEST, STAGE_PIXEL, STAGE_FINAL

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
KEYBOARD = ReplyKeyboardMarkup([["подсказка", "сначала"]], resize_keyboard=True)


def normalize(text):
    return text.strip().lower().replace("ё", "е").replace(" ", "").replace("-", "")


async def send_card(update, context, stage):
    data = QUEST[stage]
    path = ASSETS / data["image"]
    if path.exists():
        with path.open("rb") as image:
            await update.effective_message.reply_photo(photo=image)
    await update.effective_message.reply_text(data["text"], reply_markup=KEYBOARD)


async def start(update, context):
    context.user_data.clear()
    context.user_data.update(stage=STAGE_PIXEL, hint_index=0)
    intro = ASSETS / "intro.png"
    if intro.exists():
        with intro.open("rb") as image:
            await update.effective_message.reply_photo(photo=image)
    await update.effective_message.reply_text(
        "Впереди 11 заданий на логику. Специальные знания не нужны. "
        "Обсуждайте версии вместе и пишите ответы в чат. "
        "Кнопка «подсказка» даёт сначала небольшой намёк, потом более подробный.\n\n"
        "Финальная цель: получить цифру для следующей точки квеста.",
        reply_markup=KEYBOARD,
    )
    await send_card(update, context, STAGE_PIXEL)
    return STAGE_PIXEL


async def reset(update, context):
    await update.effective_message.reply_text("Окей, начинаем заново.")
    return await start(update, context)


async def handle_answer(update, context):
    stage = context.user_data.get("stage", STAGE_PIXEL)
    text = normalize(update.effective_message.text or "")
    if text in {"подсказка", "hint"}:
        hints = QUEST[stage]["hints"]
        index = min(context.user_data.get("hint_index", 0), len(hints) - 1)
        await update.effective_message.reply_text(hints[index], reply_markup=KEYBOARD)
        context.user_data["hint_index"] = index + 1
        return stage
    if text in {"сначала", "startover", "reset"}:
        return await reset(update, context)
    if text not in {normalize(answer) for answer in QUEST[stage]["answer"]}:
        await update.effective_message.reply_text(
            "Пока не совпало. Обсудите ещё одну версию или возьмите подсказку.", reply_markup=KEYBOARD)
        return stage
    await update.effective_message.reply_text(QUEST[stage]["success"], reply_markup=KEYBOARD)
    if stage == STAGE_FINAL:
        await update.effective_message.reply_text(
            "ГОТОВО.\n\nЦифра вашей аудитории: 1\n\n"
            "Покажите это сообщение организатору и двигайтесь к следующей точке.",
            reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        return ConversationHandler.END
    context.user_data.update(stage=stage + 1, hint_index=0)
    await send_card(update, context, stage + 1)
    return stage + 1


async def cancel(update, context):
    context.user_data.clear()
    await update.effective_message.reply_text(
        "Квест остановлен. Для нового запуска отправь /start.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def build_app(token):
    app = Application.builder().token(token).concurrent_updates(False).build()
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={stage: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)] for stage in QUEST},
        fallbacks=[CommandHandler("reset", reset), CommandHandler("cancel", cancel)],
        allow_reentry=True))
    app.add_handler(CommandHandler("reset", reset))
    return app


def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    load_dotenv(ROOT / ".env")
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is empty. Set it in .env.")
    asyncio.set_event_loop(asyncio.new_event_loop())
    build_app(token).run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
