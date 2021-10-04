from models.user import UserModel
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('testUser', 'pass123')

            self.assertIsNone(UserModel.find_by_username('testUser'))

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username('testUser'))
        