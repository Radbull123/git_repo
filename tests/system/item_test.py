import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.item_data = {'name': 'TestItem', 'price': 99.99, 'store_id': 1}
        user_data = {'username': 'TestUser', 'password': 'TestPassword'}
        with self.app() as client:
            with self.app_context():
                UserModel(*user_data.values()).save_to_db()
                auth = client.post(
                    '/auth',
                    data = json.dumps(user_data),
                    headers={'Content-Type': 'application/json'},
                )
                acces_token = json.loads(auth.data)['access_token']
                self.header = {'Authorization': f'JWT {acces_token}'}

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(f"/item/{self.item_data['name']}")

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data), self.item_data)

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get(f"/item/{self.item_data['name']}")

                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get(f'/item/{self.item_data["name"]}', headers=self.header)

                self.assertEqual(response.status_code, 404)
                
    def test_get_item_found(self):
        with self.app() as client:
            with self.app_context():
                ItemModel(*self.item_data.values()).save_to_db()
                self.item_data.pop('store_id')
                response = client.get(f'/item/{self.item_data["name"]}', headers=self.header)

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), self.item_data)

    def test_put_update(self):
        update_price = {'price': 20.99}
        with self.app() as client:
            with self.app_context():
                ItemModel(*self.item_data.values()).save_to_db()
                old_price_resp = client.get(f'/item/{self.item_data["name"]}', headers=self.header)

                self.assertEqual(json.loads(old_price_resp.data)['price'], self.item_data['price'])
                
                self.item_data.update(update_price) # Change the price
                
                new_price_resp = client.put(f"/item/{self.item_data['name']}", data=self.item_data)

                self.assertEqual(json.loads(new_price_resp.data)['price'], update_price['price'])

                self.item_data.pop('store_id')

                self.assertDictEqual(json.loads(new_price_resp.data), self.item_data)
                self.assertNotEqual(old_price_resp, new_price_resp)
