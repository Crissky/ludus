import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)

from bot.constants.callback import COMMAND_CLOSE_CALLBACK_DATA
from bot.decorators.logging import logging_basic_infos
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.chat import (
    delete_message,
    send_answer
)


@alert_if_not_chat_owner()
@logging_basic_infos
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fecha uma mensagem.
    """

    logging.info('CLOSE() - FECHANDO MENSAGEM')
    query = update.callback_query
    function_caller = 'CLOSE()'

    if query:
        await send_answer(
            function_caller=function_caller,
            query=query,
            text='Fechando conversa...'
        )
        await delete_message(
            function_caller=function_caller,
            context=context,
            query=query,
        )


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close,
    pattern=f'^{{"command":"{COMMAND_CLOSE_CALLBACK_DATA}"'
)
