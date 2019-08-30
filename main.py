#!/usr/bin/env python3
#
# This program runs as cronjob daily to send birthday emails to users who have birthday that day.
#
from dao import user_dao

import asyncio


async def send_email(user):
    """ Assume we are sending email.

    Using async because send mail could take longer to finish.
    """
    await print('Send email')


def next_birthday_time():
    """ Calculates seconds to the next birthday date at 00:00:00 am
    so the cron job can process on that day.
    """
    return user_dao.diff_of_one_year_from_now()


async def coro_user(key):
    """ Checks each user if they have birthday today.
        Send emails to users on their birthday and mark
        a sent flag in redis to indicate that their birthday email will
        only happen again next year.

        Args:
            key string sent key name to notify this user wont have
             another birthday before it expired.
        """
    user = user_dao.find(key)
    if user and user_dao.celebrate_birthday(user):
        # sendEmail
        send_email(user)
        user_dao.set_exp(user, next_birthday_time())


async def main(key):
    """ Creating tasks to process every user concurrently. """
    asyncio.create_task(coro_user(key))


if __name__ == "__main__":

    user_dao = user_dao.UserDao()
    for key in user_dao.get_all():
        asyncio.run(main(key))

