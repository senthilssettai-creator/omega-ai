FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl ffmpeg libnss3 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxrandr2 libxdamage1 libxfixes3 libgbm1 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install .
RUN playwright install --with-deps

COPY omega ./omega

EXPOSE 8080

CMD ["omega", "run", "--host", "0.0.0.0", "--port", "8080"]