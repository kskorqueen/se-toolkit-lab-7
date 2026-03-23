async def handle_start(args):
    return "Привет! Я LMS-бот. Используй /help для списка команд."

async def handle_help(args):
    return "/start - Приветствие\n/help - Помощь\n/health - Статус API"

async def handle_health(args):
    return "API работает нормально (заглушка)"
