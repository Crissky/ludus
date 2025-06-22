'''Arquivo principal que executa o telegram-bot.
'''

import logging
from decouple import config

from telegram.ext import Application

from bot.conversations import (
    CHOICE_TYPE_GAME_HANDLERS,
    CHOICE_GAME_HANDLERS,
)


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
MY_GROUP_ID = config('MY_GROUP_ID', cast=int)
IS_PRODUCTION = config('IS_PRODUCTION', cast=bool, default=True)
(
    DEFAULT_GROUP,
    CHAT_XP_GROUP,
    WORDGAME_GROUP,
) = range(3)


if IS_PRODUCTION:
    logging.basicConfig(
        filename='ludus.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
else:
    logging.basicConfig(
        filename='ludus.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    # application.add_handler()

    # Add Multiple Handlers
    application.add_handlers(CHOICE_TYPE_GAME_HANDLERS)
    application.add_handlers(CHOICE_GAME_HANDLERS)

    # Add Jobs
    application.job_queue.run_repeating()

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
