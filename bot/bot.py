import argparse
import asyncio
import sys
from handlers.commands import handle_start, handle_help, handle_health

async def run_test(command):
    # Карта команд
    routes = {
        "/start": handle_start,
        "/help": handle_help,
        "/health": handle_health
    }
    cmd = command.split()[0]
    handler = routes.get(cmd, lambda a: f"Неизвестная команда: {cmd}")
    print(await handler(command))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str)
    args = parser.parse_args()

    if args.test:
        asyncio.run(run_test(args.test))
    else:
        print("Здесь будет логика запуска Telegram-бота (aiogram)")
