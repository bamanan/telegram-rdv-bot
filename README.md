# Orion RDV Bot

Orion RDV Bot is a Telegram bot designed to check for available appointments on the Orion reservation system and notify users when appointments are found.

**Warning**: Orion RDV Bot uses web scraping to retrieve appointment information from the Orion reservation system. Make sure to use it responsibly and only for personal usage and avoid excessive scraping, as it may violate the terms of service of the website.

## Features

- Scrapes the Orion reservation system for available appointments
- Notifies users via Telegram when appointments are found
- Allows users to start and stop appointment checking
- Allows users to set the frequency of appointment checking

## Installation

1. Clone the repository:

```bash
git clone git@github.com:bamanan/telegram-rdv-bot.git
```

2. Generate Bot Token

Open and search on Telegram [BotFather](https://t.me/BotFather) bot and create a new Bot Token using `/newbot` command.
Copy and paste this token in the config.py or in the `docker-compose.yaml`

## Configuration

Before running the bot, make sure to configure the following variables in the `config.py` file:

- `TOKEN`: Your Telegram bot token.
- `URL`: The URL of the Orion reservation system.
- `DEFAULT_FREQUENCY`: The interval between each request to orion timetable.
- `CHROMIUM_PATH`: The path to the Chromium executable or leave it empty if using the default system path.

**Note**: Setting the frequency of appointment checking too high may result in excessive load on the Orion reservation system and could be considered as a cyber attack. Use reasonable intervals to avoid this.

## Run

Run the bot using docker 
```bash
docker-compose up --build
```


## Usage
Start the bot by sending /start command.
Use the following commands to control the bot:

- `/demarrer`: Start checking for appointments.
- `/arreter`: Stop checking for appointments.
- `/frequence <seconds>`: Set the frequency of appointment checking (in seconds).

**Note**: Setting the frequency of appointment checking too high may result in excessive load on the Orion reservation system and could be considered as a cyber attack. Use reasonable intervals to avoid this.
