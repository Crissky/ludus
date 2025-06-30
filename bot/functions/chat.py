import logging

from datetime import timedelta
from random import randint
from time import sleep
from typing import Any, Callable, Union
from bson import ObjectId

from telegram import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message
)
from telegram.constants import ChatAction, ChatType, ParseMode
from telegram.error import BadRequest, Forbidden, RetryAfter, TimedOut
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.buttons import get_close_keyboard
from bot.functions.enums.emoji import EmojiEnum


CALLBACK_CLOSE = '$close'
BASE_JOB_KWARGS = {'misfire_grace_time': None}
HOURS_DELETE_MESSAGE_FROM_CONTEXT = 4
CHAT_TYPE_GROUPS = (ChatType.GROUP, ChatType.SUPERGROUP)
MIN_AUTODELETE_TIME = timedelta(minutes=15)
HALF_AUTODELETE_TIME = timedelta(minutes=30)


# TEXTS
REPLY_MARKUP_DEFAULT = 'DEFAULT'
LEFT_CLOSE_BUTTON_TEXT = f'{EmojiEnum.CLOSE.value}Fechar'
RIGHT_CLOSE_BUTTON_TEXT = f'Fechar{EmojiEnum.CLOSE.value}'
REFRESH_BUTTON_TEXT = f'{EmojiEnum.REFRESH.value}Atualizar'
DETAIL_BUTTON_TEXT = f'{EmojiEnum.DETAIL.value}Detalhar'
VERBOSE_ARGS = ['verbose', 'v']
REPLY_CHAT_ACTION_KWARGS = dict(action=ChatAction.TYPING)


# MESSAGES FUNCTIONS
async def call_telegram_message_function(
    function_caller: str,
    function: Callable,
    context: ContextTypes.DEFAULT_TYPE,
    need_response: bool = False,
    skip_retry: bool = False,
    **kwargs
) -> Union[Any, Message]:
    '''Função que chama qualquer função de mensagem do telegram.
    Caso ocorra um erro do tipo RetryAfter ou TimedOut, a função agurdará
    alguns segundos tentará novamente com um número máximo de 3 tentativas.

    Se need_response for True, a função aguardará para realizar uma nova
    tentativa, caso contrário, a função será agendada em um job para ser
    executada posteriormente.

    Se skip_retry for True, a função não tentará novamente e nem agendará uma
    nova tentativa.
    '''

    logging.info(f'{function_caller}->CALL_TELEGRAM_MESSAGE_FUNCTION()')
    job_call_telegram_kwargs = dict(
        function_caller=function_caller,
        function=function,
        context=context,
        **kwargs
    )
    response = None
    is_error = True
    catched_error = None
    for i in range(3):
        try:
            response = await function(**kwargs)
            is_error = False
            break
        except (RetryAfter, TimedOut) as error:
            catched_error = error
            if skip_retry is True:
                break

            if isinstance(error, RetryAfter):
                sleep_time = error.retry_after + randint(1, 3)
            elif isinstance(error, TimedOut):
                sleep_time = 5

            error_name = error.__class__.__name__
            if need_response is False:
                logging.info(
                    f'{error_name}{i}({sleep_time}): '
                    f'creating JOB "{function.__name__}" '
                )
                job_name = (
                    f'{function_caller}->'
                    f'CALL_TELEGRAM_MESSAGE_FUNCTION->'
                    f'JOB_CALL_TELEGRAM-{ObjectId()}'
                )
                context.job_queue.run_once(
                    callback=job_call_telegram,
                    when=timedelta(seconds=sleep_time),
                    data=job_call_telegram_kwargs,
                    name=job_name,
                    job_kwargs=BASE_JOB_KWARGS,
                )
                return ConversationHandler.END

            logging.info(
                f'{error_name}{i}: RETRYING activate "{function.__name__}" '
                f'from {function_caller} in {sleep_time} seconds.'
            )
            sleep(sleep_time)
            continue

    if is_error is True:
        logging.error(f'ERROR: {function_caller}')
        if catched_error:
            raise catched_error
        raise Exception(f'Error in {function_caller}')

    return response


async def send_private_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    user_id: int,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = True,
    need_response: bool = False,
    skip_retry: bool = False,
) -> Message:
    ''' Tenta enviar mensagem privada, caso não consiga pelo erro "Forbidden"
    envia mensagem para o grupo marcando o nome do jogador.
    '''

    markdown = ParseMode.MARKDOWN_V2 if markdown else None
    owner_id = user_id if close_by_owner is True else None
    silent = True
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )

    try:
        call_telegram_kwargs = dict(
            chat_id=user_id,
            text=text,
            parse_mode=markdown,
            disable_notification=silent,
            reply_markup=reply_markup,
        )

        response = await call_telegram_message_function(
            function_caller='SEND_PRIVATE_MESSAGE()',
            function=context.bot.send_message,
            context=context,
            need_response=need_response,
            skip_retry=skip_retry,
            **call_telegram_kwargs
        )

        return response
    except Forbidden as error:
        logging.info(
            f'SEND_PRIVATE_MESSAGE(): Usuário {user_id} não pode '
            f'receber mensagens privadas. '
            f'Ele precisa iniciar uma conversa com o bot.\n'
            f'Function Caller: {function_caller}\n'
            f'Message: {text}\n'
            f'(ERROR: {error})'
        )


async def edit_message_text(
    function_caller: str,
    new_text: str,
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    chat_id: int = None,
    user_id: int = None,
    need_response: bool = False,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = True,
) -> Union[Message, bool]:
    '''Edita uma mensagem usando um Message ou um ContextTypes.
    '''

    chat_id = context._chat_id if chat_id is None else chat_id
    user_id = context._user_id if user_id is None else user_id
    markdown = ParseMode.MARKDOWN_V2 if markdown is True else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )
    edit_text_kwargs = dict(
        text=new_text,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=markdown,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller=f'{function_caller} -> EDIT_MESSAGE_EDIT()',
        function=context.bot.edit_message_text,
        context=context,
        need_response=need_response,
        **edit_text_kwargs
    )

    return response


# QUERY FUNCTIONS
async def delete_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
):
    '''Deleta a mensagem usando query,
    caso ocorra um erro BadRequest tenta deletar a mensagem usando o context.
    '''

    try:
        logging.info('DELETE_MESSAGE() TRYING QUERY.DELETE_MESSAGE')
        await call_telegram_message_function(
            function_caller=function_caller + ' and DELETE_MESSAGE()',
            function=query.delete_message,
            context=context,
            need_response=False,
        )
    except BadRequest as e:
        logging.info('DELETE_MESSAGE() BADREQUEST EXCEPT')
        chat_id = query.message.chat.id
        message_id = query.message.message_id
        if 'Query is too old' in e.message:
            delete_message_kwargs = dict(
                chat_id=chat_id,
                message_id=message_id
            )
            await call_telegram_message_function(
                function_caller=function_caller,
                function=context.bot.delete_message,
                context=context,
                need_response=False,
                **delete_message_kwargs
            )
        elif 'Message to delete not found' in e.message:
            logging.warning(f'\tError Message: "{e.message}"')
        else:
            raise e


async def send_answer(
    function_caller: str,
    query: CallbackQuery,
    text: str,
):
    '''Envia um answer usando uma query.
    '''

    logging.info(f'{function_caller}->SEND_ANSWER()')
    try:
        await query.answer(text=text, show_alert=False)
    except BadRequest:
        logging.info('ANSWER() BADREQUEST EXCEPT.')
        logging.warning(f'  text: {text}')


async def send_alert(
    function_caller: str,
    query: CallbackQuery,
    text: str,
):
    '''Envia um alert usando uma query.
    '''

    logging.info(f'{function_caller}->SEND_ALERT()')
    try:
        await query.answer(text=text, show_alert=True)
    except BadRequest:
        logging.info('ANSWER() BADREQUEST EXCEPT.')
        logging.warning(f'  text: {text}')


# JOB FUNCTIONS
async def job_call_telegram(context: ContextTypes.DEFAULT_TYPE):
    '''Agenda uma função call_telegram_message_function caso ocorra um erro
    do tipo RetryAfter, TimedOut e o need_response seja False
    '''

    logging.info('JOB_CALL_TELEGRAM()')
    job = context.job
    call_telegram_kwargs = job.data
    call_telegram_kwargs['function_caller'] += ' and JOB_CALL_TELEGRAM()'
    logging.info(call_telegram_kwargs['function_caller'])

    await call_telegram_message_function(**call_telegram_kwargs)
