import datetime
import sys
from random import randint
from StringIO import StringIO

import django.http
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.utils import timezone
from django.utils.importlib import import_module

import mock
import pytz

from accounts import factoryboy
from cst import utils
from cst.cypher import encode_id


class Utils(TestCase):

    def setUp(self):
        self.user = factoryboy.UserFactory(email='neal6119@gmail.com')
        self.profile = factoryboy.UserProfileFactory(user=self.user)

    def test_today(self):
        # now is defined to be 26/Nov/2016 18:10:0 UTC
        now = lambda: datetime.datetime(
            2016, 11, 26, 18, 10, 0, 0, tzinfo=timezone.utc)

        # Since HK is UTC+8:00 the if we get the date it should show 27/Nov/2016
        # that is one day ahead of UTC.
        hk_tz = pytz.timezone('Asia/Hong_Kong')
        timezone.activate(hk_tz)
        self.assertEquals(utils.today(now), datetime.date(2016, 11, 27))

        # But since India is UTC+5:30 we should still see the date to be
        # 26/Nov/2016, same day as UTC.
        india_tz = pytz.timezone('Asia/Kolkata')
        timezone.activate(india_tz)
        self.assertEquals(utils.today(now), datetime.date(2016, 11, 26))

    def test_convert_utc_to_local_time(self):
        now = datetime.datetime(2015, 10, 6, 10, 10, 0, 0, tzinfo=timezone.utc)
        india_tz = pytz.timezone('Asia/Kolkata')
        time = india_tz.localize(datetime.datetime(2015, 10, 6, 15, 40))
        self.assertEquals(utils.convert_utc_to_local_time(now), time)

    def test_convert_x_to_y(self):
        result = utils.convert_from_rangex_to_rangey(50, 0, 100, 0, 10)
        self.assertEquals(result, 5)

    def test_is_in_range(self):
        is_in_range = utils.is_in_range(0, 0, 0)
        self.assertEquals(is_in_range, True)
        is_in_range = utils.is_in_range(0, 1, 1)
        self.assertEquals(is_in_range, False)
        is_in_range = utils.is_in_range(1, 0, 1)
        self.assertEquals(is_in_range, True)
        is_in_range = utils.is_in_range(1, 0, 2)
        self.assertEquals(is_in_range, True)

    def test_list_to_text(self):
        array = ['a']
        text = utils.list_to_text(array)
        self.assertEquals(text, 'a')

    def test_list_to_text_2_items(self):
        array = ['a', 'b']
        text = utils.list_to_text(array)
        self.assertEquals(text, 'a and b')

    def test_list_to_text_3_items(self):
        array = ['a', 'b', 'c']
        text = utils.list_to_text(array)
        self.assertEquals(text, 'a, b and c')

    def test_list_to_text_4_items(self):
        array = ['a', 'b', 'c', 'd']
        text = utils.list_to_text(array)
        self.assertEquals(text, 'a, b, c and d')

    def test_valid_emails(self):
        valid_emails = ['1+2-5.8@2-8.com', 'neal6119@gmail.com', 'retail@one.co.retail.....']
        for email in valid_emails:
            self.assertTrue(utils.is_valid_email(email))

    def test_invalid_emails(self):
        invalid_emails = ['', 'oin-sihs234_@Ret-ailone', 'neal6119gmail.com', 'username']
        for email in invalid_emails:
            self.assertFalse(utils.is_valid_email(email))

    def test_x_what_percent_y(self):
        self.assertEquals(43.20987654320987, utils.x_is_what_percent_of_y(35, 81))
        self.assertEquals(50, utils.x_is_what_percent_of_y(50, 100))
        self.assertEquals(25, utils.x_is_what_percent_of_y(25, 100))
        self.assertEquals(0, utils.x_is_what_percent_of_y(0, 0))

    def test_get_user_from_username_or_email_with_username(self):
        user = utils.get_user_from_username_or_email(self.user.username)
        self.assertEquals(user.id, self.user.id)

    def test_get_user_from_username_or_email_with_email(self):
        user = utils.get_user_from_username_or_email(self.user.email)
        self.assertEquals(user.id, self.user.id)

    def test_get_user_from_username_or_email_no_user_found(self):
        try:
            utils.get_user_from_username_or_email('no.such.user')
            self.assertFail('Should have thrown User.DoesNotExist')
        except User.DoesNotExist:
            pass

    def test_get_closest_ceil(self):
        closest_ceil = utils.get_closest_higher_value(10, [9, 15, 20])
        self.assertEquals(15, closest_ceil)
        closest_ceil = utils.get_closest_higher_value(10, [10, 15, 20])
        self.assertEquals(15, closest_ceil)
        closest_ceil = utils.get_closest_higher_value(10, [1])
        self.assertEquals(-1, closest_ceil)

    def test_get_datetime_with_min_time(self):
        datetime_obj = datetime.datetime.now()
        self.assertNotEquals(datetime_obj.time(), datetime.time.min)
        new_datetime_obj = utils.get_datetime_with_min_time(datetime_obj)
        self.assertEquals(new_datetime_obj.time(), datetime.time.min)

    def test_get_datetime_with_max_time(self):
        datetime_obj = datetime.datetime.now()
        self.assertNotEquals(datetime_obj.time(), datetime.time.max)
        new_datetime_obj = utils.get_datetime_with_max_time(datetime_obj)
        self.assertEquals(new_datetime_obj.time(), datetime.time.max)

    def test_make_tz_aware(self):
        datetime_obj = datetime.datetime.now()
        self.assertTrue(datetime_obj.tzinfo is None)
        timezone_obj = utils.make_tz_aware(datetime_obj)
        self.assertTrue(timezone_obj.tzinfo is not None)

    def test_validate_international_phone_number(self):
        valid_phone_no = [
            '+919999999999', '9999999999', '+19999999999',
            '+449999999999', '09999999999', '+116500000000'
        ]
        for phone_no in valid_phone_no:
            self.assertTrue(utils.validate_international_phone_number(phone_no))

        invalid_phone_no = [
            '+91123456789', '99999999', '+199999999',
            '044999999999999', '2345.44555', '34455a4455',
            '11111111111111', '111+111111', '+9112345678910'
        ]
        for phone_no in invalid_phone_no:
            self.assertFalse(utils.validate_international_phone_number(phone_no))

    def test_remove_special_chars_from_phone_number(self):
        phone_nos = [
            '+44999$ ()999  99', '099!!999a99999', '+116500$%^)*@#000000',
            '+1-5 41-75  4-3010', '+1-54asd1(754)3asfsdg  010', '+1 541 (754) 3010',
            '', None
        ]
        expeted_phone_nos = [
            '4499999999', '09999999999', '116500000000',
            '15417543010', '15417543010', '15417543010',
            '', ''
        ]
        for (phone_no, expected_no) in zip(phone_nos, expeted_phone_nos):
            self.assertEquals(utils.remove_special_chars_from_phone_number(phone_no), expected_no)

    def test_validate_email_domain(self):
        username = 'neelanshu@xyz.com'
        domain = 'xyz.com'
        self.assertTrue(utils.validate_email_domain(username, domain))

        username = 'neelanshu@abc.retail.one'
        domain = 'retail.one'
        self.assertTrue(utils.validate_email_domain(username, domain))

        username = 'neelanshu@abcretail.one'
        domain = 'retail.one'
        self.assertFalse(utils.validate_email_domain(username, domain))

        username = 'neelanshu@Retail.One'
        domain = 'retail.one'
        self.assertTrue(utils.validate_email_domain(username, domain))

    def test_validate_email_domain_in(self):
        username = 'lol@headrun.com'
        domains = ['mieone.com', 'stockone.com']
        self.assertFalse(utils.validate_email_domain_in(username, domains))

        username = 'yay@stockone.com'
        self.assertTrue(utils.validate_email_domain_in(username, domains))

        username = 'yay@mieone.com'
        self.assertTrue(utils.validate_email_domain_in(username, domains))

    def test_get_email_domain(self):
        email = 'hhh@k.com'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, 'k.com')

        email = 'hhh@'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, None)

        email = 'abc'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, None)

        email = 'abc@f'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, None)

        email = 'abc@fg'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, 'fg')

        email = 'abc@retail.fg.com'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, 'fg.com')

        email = 'abc@g.com'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, 'g.com')

        email = 'abc@d.g.com'
        domain = utils.get_email_domain(email)
        self.assertEqual(domain, 'g.com')

    def test_get_week_monday(self):
        date = timezone.datetime(2015, 10, 8).date()
        monday_date = utils.get_week_monday(date)
        self.assertEquals(monday_date, timezone.datetime(2015, 10, 5).date())

        date = timezone.datetime(2015, 10, 5).date()
        monday_date = utils.get_week_monday(date)
        self.assertEquals(monday_date, timezone.datetime(2015, 10, 5).date())

        date = timezone.datetime(2015, 10, 4).date()
        monday_date = utils.get_week_monday(date)
        self.assertEquals(monday_date, timezone.datetime(2015, 9, 28).date())

        date = timezone.datetime(2015, 10, 4).date()
        monday_date = utils.get_week_monday(date)
        self.assertEquals(monday_date, timezone.datetime(2015, 9, 28).date())

    def test_get_week_boundary(self):
        date = timezone.datetime(2015, 10, 8).date()
        start_date, end_date = utils.get_week_boundary(date)
        self.assertEquals(start_date, timezone.datetime(2015, 10, 5).date())
        self.assertEquals(end_date, timezone.datetime(2015, 10, 11).date())

    def test_get_user_agent_string(self):
        request = RequestFactory()
        user_agent_string = utils.get_user_agent_string(request)
        self.assertEqual(user_agent_string, '')

        req = request.get('/app_deeplink')
        user_agent_string = utils.get_user_agent_string(req)
        self.assertEqual(user_agent_string, '')

        req = request.get('/app_deeplink', HTTP_USER_AGENT='Apple-Android-Firefox')
        user_agent_string = utils.get_user_agent_string(req)
        self.assertEqual(user_agent_string, 'apple-android-firefox')

    def test_get_date_string(self):
        date_1 = datetime.datetime(2015, 12, 1, tzinfo=timezone.utc)
        date_2 = datetime.datetime(2015, 12, 2, tzinfo=timezone.utc)
        date_3 = datetime.datetime(2015, 12, 3, tzinfo=timezone.utc)
        date_4 = datetime.datetime(2015, 12, 4, tzinfo=timezone.utc)

        self.assertEquals(utils.get_date_string(date_1), '1st')
        self.assertEquals(utils.get_date_string(date_2), '2nd')
        self.assertEquals(utils.get_date_string(date_3), '3rd')
        self.assertEquals(utils.get_date_string(date_4), '4th')

    def test_split_list(self):
        the_list = [1, 2, 3,]
        chunk_size = 2
        result = utils.split_list(the_list, chunk_size)
        self.assertEquals(result, [[1, 2], [3]])

        chunk_size = 10
        result = utils.split_list(the_list, chunk_size)
        self.assertEquals(result, [the_list])

        chunk_size = 0
        result = utils.split_list(the_list, chunk_size)
        self.assertEquals(result, [the_list])

        the_list = []
        chunk_size = 10
        result = utils.split_list(the_list, chunk_size)
        self.assertEquals(result, the_list)
