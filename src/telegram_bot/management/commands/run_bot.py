import os
import time

from django.core.management.base import BaseCommand
from loguru import logger

from src.telegram_bot.Bot import TelegramBot


class Command(BaseCommand):
    TELEGRAM_BOT_DIRE = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    logger.add(f"{TELEGRAM_BOT_DIRE}/logs/debug_logs/debug.log", format="{time} {level} {message}",
               level="DEBUG", rotation="2 MB", compression="zip",
               encoding="utf-8")
    logger.add(f"{TELEGRAM_BOT_DIRE}/logs/info_logs/info.log", format="{time} {level} {message}",
               level="INFO", rotation="2 MB", compression="zip",
               encoding="utf-8")
    logger.add(
        f"{TELEGRAM_BOT_DIRE}/logs/error_logs/error.log", format="{time} {level} {message}", level="ERROR",
        rotation="2 MB", compression="zip", encoding="utf-8")

    def handle(self, *args, **kwargs):
        while True:
            try:
                self.telegram_bot = TelegramBot().run()
            except Exception as ex:
                logger.exception(ex)
