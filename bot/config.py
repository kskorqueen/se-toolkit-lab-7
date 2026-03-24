import os
from dotenv import load_dotenv

# На всякий случай проверяем оба пути
load_dotenv('.env.bot.secret')
load_dotenv('../.env.bot.secret')

LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://127.0.0.1:42002").strip().rstrip('/')
LMS_API_BASE_URL = LMS_API_BASE_URL.replace("backend", "127.0.0.1").replace("localhost", "127.0.0.1")

if not LMS_API_BASE_URL.startswith("http"):
    LMS_API_BASE_URL = "http://" + LMS_API_BASE_URL

LMS_API_KEY = os.getenv("LMS_API_KEY", "").strip()
