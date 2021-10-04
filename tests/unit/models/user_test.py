from unittest import TestCase
from models.user import UserModel


class UserUnitTest(TestCase):
    def test_create_user(self):
        user = UserModel("testUser", "pass123")

        self.assertEqual(user.username, 'testUser')
        self.assertEqual(user.password, "pass123")
        