import os
from dotenv import load_dotenv

load_dotenv(".env.bot.secret")

LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL")
LMS_API_KEY = os.getenv("LMS_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
