# Telegram-квест для аудитории

Квест для первокурсников: 11 простых заданий на логику. В финале бот выдает цифру **1**.

## Быстрый запуск

1. Установи Python 3.11 или новее с сайта https://www.python.org/downloads/.
2. Создай бота через [@BotFather](https://t.me/BotFather) и получи токен.
3. Установи зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Скопируй `.env.example` в `.env` и вставь токен:

```powershell
Copy-Item .env.example .env
notepad .env
```

5. Сгенерируй картинки:

```powershell
python make_assets.py
```

6. Запусти бота:

```powershell
python bot.py
```

После установки Python открой PowerShell в папке проекта и выполни команды по порядку. Если PowerShell запрещает запуск `.ps1`, выполни один раз от имени текущего пользователя:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Как проходит квест

- `/start` запускает атмосферный бриф.
- Участники проходят 11 логических заданий.
- На каждом этапе бот принимает ответ текстом.
- Если команда застряла, можно отправить `подсказка`.
- В любой момент `/reset` начинает заново.

Ответы организатора находятся в `ORGANIZER.md`.

## Размещение на Render

В проекте уже есть `web_bot.py` и `render.yaml` для работы через webhook. В Render создай новый Web Service из репозитория, выбери бесплатный план и добавь переменные:

```text
BOT_TOKEN=новый токен от BotFather
BASE_URL=https://имя-сервиса.onrender.com
WEBHOOK_SECRET=любая длинная случайная строка
```

Команды сборки и запуска Render возьмёт из `render.yaml`. После публикации проверь адрес `https://имя-сервиса.onrender.com/`: он должен вернуть `status: ok`.
