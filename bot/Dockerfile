FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14.2-slim-bookworm

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Рабочая директория — корень проекта
WORKDIR /app

# Копируем всё
COPY . .

# Устанавливаем зависимости (используя корневой pyproject.toml)
RUN uv sync --frozen --no-cache

# ВАЖНО: Команда запуска. 
# Мы говорим uv запустить python, указывая правильный путь к файлу.
CMD ["uv", "run", "python", "bot/bot.py"]
