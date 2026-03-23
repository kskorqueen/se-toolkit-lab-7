# --- Stage 1: build the application ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Копируем всё в /app
COPY pyproject.toml uv.lock /app/
COPY backend /app/backend

# Синхронизируем зависимости (uv создаст окружение в /app/.venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# --- Stage 2: final image ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot && \
    useradd --system --gid 999 --uid 999 --create-home nonroot

# Копируем всё из билдера
COPY --from=builder --chown=nonroot:nonroot /app /app

# Исправленный путь к PATH (без слова backend)
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
# Работаем из папки backend, чтобы uvicorn видел папку app
WORKDIR /app/backend

# ЗАПУСК: указываем прямой путь к python в корневой папке /app/.venv
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]