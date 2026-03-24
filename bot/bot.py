import sys
import argparse
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем обработчики из твоего файла
from handlers.core.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores

# Загружаем токен
load_dotenv('../.env.bot.secret')
TOKEN = os.getenv("BOT_TOKEN")

# Функции-обертки для Telegram
async def tg_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(handle_start())

async def tg_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(handle_help())

async def tg_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(handle_health())

async def tg_labs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(handle_labs())

async def tg_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Берем аргументы после команды /scores
    args = " ".join(context.args)
    await update.message.reply_text(handle_scores(args))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run a command in test mode")
    args, _ = parser.parse_known_args()

    # РЕЖИМ ТЕСТА (для авточекера)
    if args.test:
        cmd_parts = args.test.strip().split(" ", 1)
        cmd = cmd_parts[0]
        cmd_args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if cmd == "/start": print(handle_start())
        elif cmd == "/help": print(handle_help())
        elif cmd == "/health": print(handle_health())
        elif cmd == "/labs": print(handle_labs())
        elif cmd == "/scores": print(handle_scores(cmd_args))
        else: print("Unknown command")
        sys.exit(0)

    # РЕЖИМ TELEGRAM (живой бот)
    if not TOKEN:
        print("Error: BOT_TOKEN not found in .env.bot.secret")
        sys.exit(1)

    print("Bot is starting in Telegram mode... Press Ctrl+C to stop.")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(CommandHandler("help", tg_help))
    app.add_handler(CommandHandler("health", tg_health))
    app.add_handler(CommandHandler("labs", tg_labs))
    app.add_handler(CommandHandler("scores", tg_scores))
    
    app.run_polling()

if __name__ == "__main__":
    main()
