#!/usr/bin/python3
from dao import user
from datetime import datetime
from dateutil.relativedelta import relativedelta

import redis


class UserDao(object):
    """ Provides business logic to user. """

    USER_NAME = 'user-%s'
    SEARCH_NAME = 'user-*'
    SENT_NAME = 'sent-%s'

    redis = None

    def __init__(self):
        """ Initialize redis connection before any function can be used. """
        self.redis = redis.StrictRedis(host='localhost', port=6379,
                                 db=0, encoding='utf-8', decode_responses=True)

    def find(self, key_name):
        """ Looks up users from the redis store.

        Args:
            key_name string
        Returns:
            user if exists or None if not exists
        """
        user_id = int(key_name.split('-')[1])
        birthday = self.redis.hget(key_name, user_id)
        if birthday:
            return user.User(user_id, birthday)
        return None

    def save(self, user):
        """ Stores user to the redis store.

        Args:
            user object includes user_id and birthday
        """
        user_id = user.get_id()
        key_name = self.USER_NAME % user_id
        self.redis.hset(key_name, user_id, user.get_birthday())

    def is_birthday(self, user, date):
        """ Checks if the date is user's birthday.

        Args:
            user object includes user_id and birthday.
            date string birthday reference.
        Returns:
            True boolean if date is user's birthday or False if its not.
        """
        if not self.in_countdown(user):
            return date == user.get_birthday()
        return False

    def set_exp(self, user, diff):
        """ Sets the countdown until the next birthday date.
        The task only needs to check users' birthday once the countdown finished.

        Args:
            user object includes user_id and birthday.
            diff integer seconds to the next birthday date.
        """
        key_name = self.SENT_NAME % user.get_id()
        self.redis.setex(key_name, diff, user.get_id())

    def in_countdown(self, user):
        """ Checks if users' next birthday is still in the countdown period.
        No need to do anything if its still in this period.

        Args:
            user object includes user_id and birthday.
        Returns:
            True boolean countdown period, no need to check birthday.
            False boolean finished countdown, check for birthday.
        """
        key_name = self.SENT_NAME % user.get_id()
        user_id = self.redis.get(key_name)
        if user_id:
            return True
        else:
            return False

    def celebrate_birthday(self, user):
        """ Checks if today is user's birthday.

        Args:
            user object includes user_id and birthday.
        Returns:
            True if its user's birthday or False if its not.
        """
        if self.is_birthday(user, datetime.now()):
            return True
        else:
            return False

    def get_all(self):
        """ Gets all users keys from the redis store.

        Returns:
            keys string that can get users.
        """
        return self.redis.keys(self.SEARCH_NAME)


def diff_of_one_year_from_now():
    """ Calculates seconds to the next birthday.
    Its more accurate to count the difference from the targeted date so
    We don't dealing with leap year and leap month issue.
    We can also just set the target date using user's birthday.
    Sets it to 00:00:00 am so the cron job wont skip this user on the birthday.
    We can also consider timezone which we just skipped in here.

    Returns:
        seconds numeric time to one year later.
    """
    now = datetime.now()
    one_year_from_now = now + relativedelta(years=1)
    new_date = datetime.date(one_year_from_now.year,
                             one_year_from_now.month,
                             one_year_from_now.day, 0, 0, 0)
    return (new_date - now).seconds
