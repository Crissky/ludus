import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.chat import send_alert


def alert_if_not_chat_owner(
    retry_state=ConversationHandler.END,
    alert_text='⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔'
):
    '''Não executa a ação quando o botão é clicado por um usuário que não
    seja o dono da mensagem e envia um alerta para o usuário que clicou no
    botão.'''

    def decorator(callback):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            logging.info('@SKIP_IF_NOT_CHAT_OWNER')
            user_id = update.effective_user.id
            query = update.callback_query

            if query:
                data = eval(query.data)
                data_user_id = data['user_id']
                if data_user_id != user_id and data_user_id is not None:
                    if isinstance(alert_text, str):
                        await send_alert(
                            function_caller='@ALERT_IF_NOT_CHAT_OWNER',
                            query=query,
                            text=alert_text,
                        )
                    return retry_state

            return await callback(update, context)

        return wrapper
    return decorator
