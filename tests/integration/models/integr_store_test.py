from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store  = StoreModel('test')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 19.99, 1)

            item.save_to_db()
            store.save_to_db()
            self.assertEqual(store.items.count(), 1)

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

