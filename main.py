import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config
from bot_manager import BotManager

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

bot_manager = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Menu:\n"
        "1. Démarrer la vérification des RDV : /demarrer\n"
        "2. Arrêter la vérification des RDV : /arreter\n"
        "3. Définir la fréquence : /frequence <seconds>\n"
    )


async def demarrer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    response = bot_manager.start_checking(chat_id)
    await update.message.reply_text(response)


async def arreter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    response = bot_manager.stop_checking(chat_id)
    await update.message.reply_text(response)


async def frequence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    try:
        interval = int(context.args[0])
        response = bot_manager.set_frequency(chat_id, interval)
        await update.message.reply_text(response)
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /frequence <seconds>")


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()
    bot_manager = BotManager(application.job_queue)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("demarrer", demarrer))
    application.add_handler(CommandHandler("arreter", arreter))
    application.add_handler(CommandHandler("frequence", frequence))

    application.run_polling()
