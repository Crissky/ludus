from datetime import datetime, timezone, timedelta
import logging
from random import randint


MIN_ADD_MINUTES = 5
MAX_ADD_MINUTES = 10


def get_brazil_time_now() -> datetime:
    utc_minus_3 = timezone(timedelta(hours=-3))
    dt = datetime.now(utc_minus_3)

    return dt


def utc_to_brazil_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = replace_tzinfo(dt)
        # delta = timedelta(hours=3)
        # dt = dt - delta
    else:
        utc_minus_3 = timezone(timedelta(hours=-3))
        dt = dt.astimezone(utc_minus_3)

    return dt


def datetime_to_string(dt: datetime) -> str:
    dt = dt.strftime("%d/%m/%Y %H:%M:%S")

    return dt


def brazil_to_utc_datetime(dt: datetime) -> datetime:
    dt = replace_tzinfo(dt)
    delta = timedelta(hours=3)

    return dt + delta


def add_random_minutes_now(dt: datetime = None) -> datetime:
    if not dt:
        dt = get_brazil_time_now()
    # dt = replace_tzinfo(dt)
    minutes = randint(MIN_ADD_MINUTES, MAX_ADD_MINUTES)
    logging.info(f"Adding {minutes} minutes")

    return dt + timedelta(minutes=minutes)


def replace_tzinfo(dt: datetime) -> datetime:
    utc = timezone(timedelta(hours=0))

    return dt.replace(tzinfo=utc)


def get_last_hour() -> datetime:
    now = datetime.now()
    next_hour = now.replace(microsecond=0, second=0, minute=0)

    return next_hour


def get_midnight_hour(get_yesterday: bool = False) -> datetime:
    now = get_brazil_time_now()
    midnight_hour = now.replace(microsecond=0, second=0, minute=0, hour=3)

    if get_yesterday:
        midnight_hour = midnight_hour - timedelta(days=1)

    return midnight_hour


def adjust_season_datetime(input_datetime: datetime) -> datetime:
    '''Adiciona 1 ano ao datetime fornecido se a data já passou em relação ao
    momento atual.
    Caso contrário, retorna o mesmo datetime sem alterações.
    '''

    logging.debug('START ADJUST_DATETIME:', input_datetime)
    now = get_brazil_time_now()
    if replace_tzinfo(input_datetime) <= now:
        try:
            new_year = input_datetime.year + 1
            if new_year < now.year:
                new_year = now.year
            input_datetime = input_datetime.replace(year=new_year)
            input_datetime = adjust_season_datetime(input_datetime)
        except ValueError:
            # Trata datas como 29 de fevereiro em anos não bissextos
            input_datetime = input_datetime + timedelta(days=366)
            input_datetime = adjust_season_datetime(input_datetime)
    logging.debug('END ADJUST_DATETIME:', input_datetime)

    return input_datetime


if __name__ == '__main__':
    logging.info(get_brazil_time_now())
    logging.info(get_midnight_hour())
    logging.info(get_midnight_hour(True))

    data_teste = datetime(2020, 2, 29, 15, 30)
    logging.info('data_teste:', data_teste)
    logging.info(adjust_season_datetime(data_teste))
