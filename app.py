"""Arquivo principal que executa o telegram-bot."""

import logging
from decouple import config

from telegram.ext import Application

from bot.conversations import (
    CLOSE_MSG_HANDLER,
)
from bot.conversations import (
    CHOICE_GAME_HANDLERS,
    PLAY_GAME_HANDLERS,
)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
# MY_GROUP_ID = config("MY_GROUP_ID", cast=int)
IS_PRODUCTION = config("IS_PRODUCTION", cast=bool, default=True)
(
    DEFAULT_GROUP,
    CHAT_XP_GROUP,
    WORDGAME_GROUP,
) = range(3)

# SET LOGGING ================================================================
if IS_PRODUCTION:
    level = logging.INFO
else:
    level = logging.DEBUG

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler("ludus.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(level)

root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
# SET LOGGING ================================================================

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""

    logger.info("INICIANDO LUDUS...")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    logger.info("Handlers adicionados.")
    # Add Single Handler
    application.add_handler(CLOSE_MSG_HANDLER)

    # Add Multiple Handlers
    application.add_handlers(CHOICE_GAME_HANDLERS)
    application.add_handlers(PLAY_GAME_HANDLERS)

    # Add Jobs
    # application.job_queue.run_repeating()

    logger.info("LUDUS iniciado com sucesso!")
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
