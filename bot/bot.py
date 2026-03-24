import sys
import argparse
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

import config
from handlers.core.llm import handle_query

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("What labs are available?", callback_data="what labs are available?")],
        [InlineKeyboardButton("Which lab has the lowest pass rate?", callback_data="which lab has the lowest pass rate?")],
        [InlineKeyboardButton("Show top 5 students in lab-04", callback_data="who are the top 5 students in lab-04?")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! I am your course assistant. Ask me anything or choose a query below:", 
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    response = await handle_query(query)
    await update.message.reply_text(response)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(f"Running Query: {query} ...")
    response = await handle_query(query)
    await update.callback_query.message.reply_text(response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Test a query in CLI")
    args = parser.parse_args()

    if args.test:
        # Для тестов в CLI запускаем асинхронную функцию вручную
        print(asyncio.run(handle_query(args.test)))
        return

    if not config.TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN is not set! Check your .env file.", file=sys.stderr)
        sys.exit(1)

    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Running in Telegram mode...", file=sys.stderr)
    # run_polling() - синхронная блокирующая функция, await перед ней не нужен!
    app.run_polling()

if __name__ == "__main__":
    main()
