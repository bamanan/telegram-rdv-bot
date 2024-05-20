import logging
from typing import Dict

from bs4 import BeautifulSoup
from pyppeteer import launch
from telegram.ext import CallbackContext, JobQueue

import config


class BotManager:
    def __init__(self, job_queue: JobQueue):
        self.job_queue = job_queue
        self.jobs: Dict[int, any] = {}  # Maps chat_id to job

    async def scraper(self):
        browser = await launch(
            {
                "headless": True,
                "executablePath": config.CHROMIUM_PATH,
                "args": ["--no-sandbox", "--disable-setuid-sandbox"],
            }
        )
        page = await browser.newPage()
        await page.goto(config.URL)

        # Wait for the rdv-calendar calendar class
        await page.waitForSelector(".rdv-calendar.calendar", {"visible": True})

        # Check for error message from the user
        error_msg = await page.evaluate(
            'document.querySelector(".user-msg.error")?.textContent'
        )
        if error_msg:
            print("User error message:", error_msg)
            await browser.close()
            return ""

        # Wait for the day-column class
        await page.waitForSelector("div.day-column", {"visible": True})

        html_content = await page.content()
        await browser.close()
        return html_content

    async def check_appointments(self, context: CallbackContext):
        try:
            html_content = await self.scraper()
            soup = BeautifulSoup(html_content, "html.parser")
            day_columns = soup.find_all("div", class_="day-column ng-star-inserted")
            available_slots = []
            for day_column in day_columns:
                day_header = day_column.find_previous("div", class_="day-header")
                day_date = day_header.find("div", class_="header-date").text.strip()
                slots = day_column.find_all("li", class_="time-slot")
                for slot in slots:
                    slot_time = slot.find("span", class_="hour").text.strip()
                    slot_location = slot.find("div", class_="site-name").text.strip()
                    available_slots.append(
                        f"{day_date} - {slot_time} à {slot_location}"
                    )
                    available_slots = set(available_slots)

            if available_slots:
                message = (
                    f"{len(available_slots)} rendez-vous disponibles !\n"
                    + "\n".join(available_slots)
                )
                await context.bot.send_message(chat_id=context._chat_id, text=message)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    def start_checking(self, chat_id: int):
        if chat_id in self.jobs:
            return "La vérification des rendez-vous est déjà en cours."
        job = self.job_queue.run_repeating(
            self.check_appointments,
            interval=config.DEFAULT_FREQUENCY,
            first=10,
            chat_id=chat_id,
        )
        self.jobs[chat_id] = job
        return (
            f"Recherche des RDV en cours, fréquence par défaut : {config.DEFAULT_FREQUENCY // 60} min. "
            "Vous pouvez modifier la fréquence en faisant /frequence <seconds>."
        )

    def stop_checking(self, chat_id: int):
        if chat_id not in self.jobs:
            return "La recherche de RDV est à l'arrêt. Pour démarrer, saisissez la commande /demarrer."
        self.jobs[chat_id].schedule_removal()
        del self.jobs[chat_id]
        return "La vérification des rendez-vous a été arrêtée."

    def set_frequency(self, chat_id: int, interval: int):
        if chat_id not in self.jobs:
            return "La recherche de RDV est à l'arrêt. Pour démarrer, saisissez la commande /demarrer."
        self.jobs[chat_id].schedule_removal()
        job = self.job_queue.run_repeating(
            self.check_appointments,
            interval=interval,
            chat_id=chat_id,
        )
        self.jobs[chat_id] = job
        return f"Votre fréquence a été modifiée avec succès. Le bot recherchera des RDV chaque {interval} secondes et vous notifiera s'il trouve un RDV."
