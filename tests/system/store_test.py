import json

from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.store_data = {
            'name': 'TestStore',
            'items': [],
        }

    def test_create_store(self):

        with self.app() as client:
            with self.app_context():
                response = client.post(f'/store/{self.store_data["name"]}')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name(self.store_data['name']))
                self.assertDictEqual(json.loads(response.data), self.store_data)

    def test_dublicate_store(self):
        tries = 2 # How many tries has ro be execute
        expected_message = {'message': f"A store with name '{self.store_data['name']}' already exists."}
        with self.app() as client:
            with self.app_context():
                for _ in range(tries):
                    response = client.post(f'/store/{self.store_data["name"]}')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data), expected_message)

    def test_delete_store(self):
        tries = 2 # How many tries has ro be execute
        expected_message = {'message': 'Store deleted'}
        with self.app() as client:
            with self.app_context():
                for idx in range(tries):
                    response = client.post(f'/store/{self.store_data["name"]}') if idx == 0 \
                        else client.delete(f'/store/{self.store_data["name"]}')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected_message)

    def test_store_list_with_items(self):
        store_id = 1
        item_data = {'name': 'TestItem', 'price': 99.99}
        self.store_data.update({'items': [item_data]})
        with self.app() as client:
            with self.app_context():
                StoreModel(self.store_data['name']).save_to_db()
                ItemModel(*item_data.values(), store_id).save_to_db()

                response = client.get(f'/store/{self.store_data["name"]}')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), self.store_data)
                

    def test_find_store(self):
            with self.app() as client:
                with self.app_context():
                    StoreModel(self.store_data['name']).save_to_db()
                    response = client.get(f'/store/{self.store_data["name"]}')
                    self.assertEqual(response.status_code, 200)
                    self.assertDictEqual(json.loads(response.data), self.store_data)

    def test_get_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel(self.store_data['name']).save_to_db()

                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'stores': [self.store_data]})