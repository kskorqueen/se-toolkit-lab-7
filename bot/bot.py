import sys
import argparse
from handlers.core.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores

def process_command(cmd_string):
    parts = cmd_string.strip().split(" ", 1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    if cmd == "/start": return handle_start()
    if cmd == "/help": return handle_help()
    if cmd == "/health": return handle_health()
    if cmd == "/labs": return handle_labs()
    if cmd == "/scores": return handle_scores(args)
    return "Unknown command. Try /help."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run a command in test mode")
    args, _ = parser.parse_known_args()

    if args.test:
        print(process_command(args.test))
        sys.exit(0)

    print("Bot is starting (production mode)...")

if __name__ == "__main__":
    main()
