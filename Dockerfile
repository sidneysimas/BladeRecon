FROM python:3.11-slim

LABEL org.opencontainers.image.title="BladeRecon" \
      org.opencontainers.image.description="Lightweight reconnaissance framework for attack-surface discovery and reporting." \
      org.opencontainers.image.version="0.2.0" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/mohamedxk9tb/BladeRecon"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md requirements.txt setup.py ./
COPY bladerecon ./bladerecon
COPY config.yaml ./config.yaml

RUN python -m pip install --upgrade pip \
    && python -m pip install .

RUN useradd --create-home --shell /usr/sbin/nologin bladerecon \
    && mkdir -p /app/results \
    && chown -R bladerecon:bladerecon /app

USER bladerecon

VOLUME ["/app/results"]

ENTRYPOINT ["bladerecon"]
CMD ["--help"]
