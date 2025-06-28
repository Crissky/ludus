
import unittest
from datetime import datetime, timedelta, timezone
from bot.functions.date_time import (
    get_brazil_time_now,
    utc_to_brazil_datetime,
    datetime_to_string,
    brazil_to_utc_datetime,
    add_random_minutes_now,
    replace_tzinfo,
    get_last_hour,
    get_midnight_hour,
    adjust_season_datetime,
)


class TestDateTimeFunctions(unittest.TestCase):
    def setUp(self):
        self.utc_tz = timezone(timedelta(hours=0))
        self.date = datetime(2023, 1, 1, 12, 30)
        self.brazil_date = datetime(2023, 1, 1, 9, 30)
        self.utc_date = datetime(2023, 1, 1, 12, 0, tzinfo=self.utc_tz)
        self.now = datetime.now()

    def test_get_brazil_time_now(self):
        ''' Teste se get_brazil_time_now retorna o horário com UTC-3.
        '''

        brazil_time = get_brazil_time_now()
        self.assertIsNotNone(brazil_time.tzinfo)
        utc_now = datetime.utcnow().replace(tzinfo=None)
        brazil_time_no_tz = brazil_time.replace(tzinfo=None)
        self.assertLess(abs(brazil_time_no_tz - utc_now), timedelta(hours=4))
        self.assertEqual(abs(brazil_time_no_tz - utc_now), timedelta(hours=3))

    def test_utc_to_brazil_datetime(self):
        '''Testa se utc_to_brazil_datetime diminui 3 horas.
        '''

        utc_time = self.utc_date
        brazil_time = utc_to_brazil_datetime(utc_time)
        self.assertEqual(brazil_time.hour, 9)
        self.assertIsNotNone(brazil_time.tzinfo)

    def test_utc_to_brazil_datetime_no_timezone(self):
        '''Testa se utc_to_brazil_datetime não diminui 3 horas quando datetime
        não tem timezone.
        '''

        utc_time = datetime(2023, 1, 1, 12, 0, tzinfo=None)
        brazil_time = utc_to_brazil_datetime(utc_time)
        self.assertEqual(brazil_time.hour, 12)
        self.assertIsNotNone(brazil_time.tzinfo)

    def test_datetime_to_string(self):
        '''Teste se datetime_to_string retorna uma string com formato
        brasileiro (dd/mm/aaaa hh/mm/ss).
        '''

        test_date = self.date
        date_str = datetime_to_string(test_date)
        self.assertEqual(date_str, "01/01/2023 12:30:00")

    def test_brazil_to_utc_datetime(self):
        '''Teste se brazil_to_utc_datetime adiciona 3 horas.
        '''

        brazil_time = self.brazil_date
        utc_time = brazil_to_utc_datetime(brazil_time)
        self.assertEqual(utc_time.hour, 12)
        self.assertIsNotNone(utc_time.tzinfo)

    def test_add_random_minutes_now(self):
        '''Teste se add_random_minutes_now adiciona entre 5 e 10 minutos a data
        fornecida, ou a data atual se nenhuma data for fornecida.
        '''

        td = timedelta(minutes=11)
        original_time = get_brazil_time_now()
        new_time1 = add_random_minutes_now()
        new_time2 = add_random_minutes_now(original_time)
        self.assertGreater(new_time1, original_time)
        self.assertGreater(new_time2, original_time)
        self.assertLess(new_time1 - original_time, td)
        self.assertLess(new_time2 - original_time, td)

    def test_replace_tzinfo(self):
        '''Teste se replace_tzinfo adiciona timezone 0 horas.
        '''

        utc = self.utc_tz
        naive_dt = self.date
        aware_dt = replace_tzinfo(naive_dt)
        self.assertIsNotNone(aware_dt.tzinfo)
        self.assertEqual(aware_dt.tzinfo, utc)
        self.assertEqual(
            naive_dt.replace(tzinfo=None),
            aware_dt.replace(tzinfo=None)
        )

    def test_get_last_hour(self):
        '''Teste se get_last_hour retorna um datetime com a hora e minuto
        sempre zero.
        '''

        current = self.now
        last_hour = get_last_hour()
        self.assertEqual(last_hour.hour, current.hour)
        self.assertEqual(last_hour.minute, 0)

    def test_get_midnight_hour(self):
        '''Teste se get_midnight_hour retorna a meia noite em UTC, mas no
        horário do Brasil, ou seja, 03:00:00
        '''

        test_date = self.date
        midnight = get_midnight_hour(test_date)
        self.assertEqual(midnight.hour, 3)
        self.assertEqual(midnight.minute, 0)
        self.assertEqual(midnight.second, 0)

    def test_adjust_season_datetime(self):
        '''Teste se adjust_season_datetime
        '''

        winter_date = datetime(2023, 1, 1, 12, 0)
        summer_date = datetime(2023, 7, 1, 12, 0)

        adjusted_winter = adjust_season_datetime(winter_date)
        adjusted_summer = adjust_season_datetime(summer_date)

        self.assertNotEqual(adjusted_winter, adjusted_summer)
        self.assertEqual(adjusted_winter.month, 1)
        self.assertEqual(adjusted_summer.month, 7)
        self.assertGreater(adjusted_winter.year, 2023)
        self.assertGreater(adjusted_summer.year, 2023)
