FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    gnupg \
    software-properties-common \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/server

RUN mkdir -p /app/output

ENV ENTOR="DOCKER"
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

EXPOSE 8000

# Arrancamos uvicorn apuntando a server.main:app
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

