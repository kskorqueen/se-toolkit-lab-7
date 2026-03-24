import sys
import argparse
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import config
from handlers.core.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores
from handlers.core.llm import handle_query

async def tg_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Available Labs", callback_data='labs'),
         InlineKeyboardButton("Backend Health", callback_data='health')],
        [InlineKeyboardButton("Top Learners (Lab 4)", callback_data='top_4')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(handle_start(), reply_markup=reply_markup)

async def tg_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если это текстовое сообщение (не команда), отправляем в LLM
    text = update.message.text
    wait_msg = await update.message.reply_text("Thinking...")
    response = await handle_query(text)
    await wait_msg.edit_text(response)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run a command in test mode")
    args = parser.parse_args()

    if args.test:
        # В тестовом режиме проверяем, не вопрос ли это к LLM
        if args.test.startswith("/"):
            cmd = args.test.split()[0]
            cmd_args = args.test.split()[1:] if len(args.test.split()) > 1 else ""
            if cmd == "/start": print(handle_start())
            elif cmd == "/help": print(handle_help())
            elif cmd == "/health": print(handle_health())
            elif cmd == "/labs": print(handle_labs())
            elif cmd == "/scores": print(handle_scores(" ".join(cmd_args)))
        else:
            # Обычный текст идет в LLM
            print(await handle_query(args.test))
        return

    # Запуск Telegram бота
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handle_help())))
    app.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(handle_health())))
    app.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(handle_labs())))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tg_message))
    
    print("Bot is starting in Telegram mode...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
