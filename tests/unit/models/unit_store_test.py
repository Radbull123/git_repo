from models.store import StoreModel
from unittest import TestCase

class UnitStoreTest(TestCase):
    def test_store_crud(self):
        store = StoreModel('test')
        self.assertEqual(store.name, 'test')
