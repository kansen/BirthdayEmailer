from dao import user, user_dao
from datetime import datetime

import time
import unittest


class TestUserDao(unittest.TestCase):
    USER_NAME = user_dao.UserDao.USER_NAME
    SENT_NAME = user_dao.UserDao.SENT_NAME
    birthday = datetime.now().strftime('%Y-%m-%d')
    ID = 1
    NUMBER_OF_USER = 10
    TEST_DIFF_SECONDS = 5

    def setUp(self):
        self.user_dao = user_dao.UserDao()
        for i in range(0, self.NUMBER_OF_USER):
            u = user.User(i, self.birthday)
            self.user_dao.save(u)
        self.test_user = user.User(self.ID, self.birthday)

    def test_find(self):
        u = self.user_dao.find(self.USER_NAME % self.ID)
        self.assertEqual(u.get_id(), self.ID)
        self.assertEqual(u.get_birthday(), self.birthday)

    def test_save(self):
        self.user_dao.save(self.test_user)
        u = self.user_dao.find(self.USER_NAME % self.ID)
        self.assertEqual(u.get_id(), self.ID)
        self.assertEqual(u.get_birthday(), self.birthday)

    def test_is_birthday(self):
        u = self.user_dao.find(self.USER_NAME % self.ID)
        self.assertTrue(self.user_dao.is_birthday(u, self.birthday))

    def test_set_exp(self):
        self.user_dao.set_exp(self.test_user, self.TEST_DIFF_SECONDS)
        time.sleep(2)
        self.assertTrue(self.user_dao.in_countdown(self.test_user))
        time.sleep(3)
        self.assertFalse(self.user_dao.in_countdown(self.test_user))

    def test_in_countdown(self):
        self.user_dao.set_exp(self.test_user, self.TEST_DIFF_SECONDS)
        time.sleep(2)
        self.assertTrue(self.user_dao.in_countdown(self.test_user))
        time.sleep(3)
        self.assertFalse(self.user_dao.in_countdown(self.test_user))

    def test_celebrate_birthday(self):
        self.user_dao.celebrate_birthday(self.test_user)

    def test_get_all(self):
        key_list = self.user_dao.get_all()
        self.assertEqual(self.NUMBER_OF_USER, len(key_list))


if __name__ == '__main__':
    unittest.main()
