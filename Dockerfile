FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Install Chromium and other necessary dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libappindicator1 \
    xdg-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y chromium chromium-driver

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Chromium's path is set correctly for pyppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Run the bot
CMD ["python", "main.py"]
