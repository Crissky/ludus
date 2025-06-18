'''Arquivo principal que executa o telegram-bot.
'''

from decouple import config

from telegram.ext import Application

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
MY_GROUP_ID = config('MY_GROUP_ID', cast=int)
(
    DEFAULT_GROUP,
    CHAT_XP_GROUP,
    WORDGAME_GROUP,
) = range(3)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler
    # application.add_handler()

    # Add Multiple Handlers
    # application.add_handlers()

    # Add Jobs
    application.job_queue.run_repeating()

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
