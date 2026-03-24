import os
from dotenv import load_dotenv

# Ищем файл в текущей папке ИЛИ в папке выше (на уровень выше)
if os.path.exists(".env.bot.secret"):
    load_dotenv(".env.bot.secret")
elif os.path.exists("../.env.bot.secret"):
    load_dotenv("../.env.bot.secret")

LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
LMS_API_KEY = os.getenv("LMS_API_KEY")

LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "coder-model")

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка загрузки (для отладки)
if not LLM_API_KEY:
    print("WARNING: LLM_API_KEY is not set! Check your .env.bot.secret path.")
