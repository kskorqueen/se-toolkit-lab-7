import sys
import argparse
from handlers.commands import handle_start, handle_help, handle_unknown

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run a command in test mode")
    # Используем parse_known_args чтобы не падать при неизвестных аргументах
    args, unknown = parser.parse_known_args()

    if args.test:
        if args.test.startswith("/start"):
            print(handle_start())
        elif args.test.startswith("/help"):
            print(handle_help())
        else:
            print(handle_unknown())
        sys.exit(0)
    else:
        print("Telegram bot is starting (production mode)...")

if __name__ == "__main__":
    main()
