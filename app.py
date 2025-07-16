"""Arquivo principal que executa o telegram-bot.
"""

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

# SET LOGGING
logger = logging.getLogger()
if IS_PRODUCTION:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("ludus.log", mode="w")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
file_handler.stream.reconfigure(encoding='utf-8')
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    application.add_handler(CLOSE_MSG_HANDLER)

    # Add Multiple Handlers
    application.add_handlers(CHOICE_GAME_HANDLERS)
    application.add_handlers(PLAY_GAME_HANDLERS)

    # Add Jobs
    # application.job_queue.run_repeating()

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
