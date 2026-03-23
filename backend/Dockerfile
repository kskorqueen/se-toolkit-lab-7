# Adapted from https://github.com/astral-sh/uv-docker-example/blob/fa761744819c05f4ce207bde1f0a396f6be3915f/multistage.Dockerfile
# Also see https://docs.astral.sh/uv/guides/integration/docker/

# ---
# --- Stage 1: build the application ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Копируем backend и pyproject.toml
COPY backend /app/backend
COPY pyproject.toml uv.lock /app/

# Работаем внутри backend
WORKDIR /app/backend

RUN python3 -m ensurepip --upgrade \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install --upgrade uv
    
# Синхронизируем зависимости uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# --- Stage 2: final image ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Создаём непользовательскую учётку
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Копируем backend из билдера
COPY --from=builder --chown=nonroot:nonroot /app /app

# Добавляем venv из builder в PATH
ENV PATH="/app/backend/.venv/bin:$PATH"

# Переключаемся на непользовательскую учётку
USER nonroot

# Рабочая директория
WORKDIR /app/backend

# CMD — путь до run.py относительно WORKDIR
CMD ["python", "run.py"]