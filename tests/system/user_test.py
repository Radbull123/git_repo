from flask.json import jsonify
from models.user import UserModel
import json
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'testUser', 'password': 'pass123'})
                self.assertEqual(request.status_code, 201)


    def test_user_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'testUser', 'password': 'pass123'})
                auth_request = client.post(
                    '/auth', 
                    data=json.dumps({'username': 'testUser', 'password': 'pass123'}),
                    headers={'Content-Type': 'application/json'},
                )

                self.assertIn('access_token', json.loads(auth_request.data).keys())


    def test_user_already_exists(self):
        pass