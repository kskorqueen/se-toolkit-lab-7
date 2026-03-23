# --- Stage 1: build the application ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Копируем файлы конфигурации зависимостей
COPY pyproject.toml uv.lock /app/
COPY backend /app/backend

WORKDIR /app/backend

# Синхронизируем зависимости (создастся окружение в /app/.venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# --- Stage 2: final image ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Создаем пользователя без прав root для безопасности
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Копируем готовое окружение и код из первого стейджа
COPY --from=builder --chown=nonroot:nonroot /app /app

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app/backend

# ИСПРАВЛЕННАЯ СТРОКА С ПРОБЕЛОМ (используем стандартный FastAPI CLI)
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]