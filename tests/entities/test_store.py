import unittest
from datetime import date
from unittest.mock import MagicMock
from api.domain.entities.store import Store
from api.enums.store_type import StoreType


class TestStore(unittest.TestCase):

    def setUp(self):
        self.mock_address = MagicMock()
        self.mock_user = MagicMock()

        self.store_kwargs = {
            'cnpj': '12345678000199',
            'address': self.mock_address,
            'reputation': 4.5,
            'trade_name': 'Test Trade',
            'legal_name': 'Test Legal Name',
            'owner': self.mock_user,
            'legal_phone_contact': '1234567890',
            'preferred_phone_contact': '0987654321',
            'legal_email_contact': 'legal@example.com',
            'preferred_email_contact': 'preferred@example.com',
            'store_type': StoreType.RETAILER,
            'opening_date': date(2020, 1, 1),
            'size': 'Large',
            'legal_nature': 'Legal Nature',
            'cnae_code': '1234',
            'branch_classification': 'Classification',
            'images': ['image1.jpg', 'image2.jpg']
        }

    def test_init_sets_all_properties(self) -> None:
        store = Store(**self.store_kwargs)
        self.assertEqual(store.cnpj, self.store_kwargs['cnpj'])
        self.assertEqual(store.address, self.mock_address)
        self.assertEqual(store.reputation, self.store_kwargs['reputation'])
        self.assertEqual(store.trade_name, self.store_kwargs['trade_name'])
        self.assertEqual(store.legal_name, self.store_kwargs['legal_name'])
        self.assertEqual(store.owner, self.mock_user)
        self.assertEqual(store.legal_phone_contact, self.store_kwargs['legal_phone_contact'])
        self.assertEqual(store.preferred_phone_contact, self.store_kwargs['preferred_phone_contact'])
        self.assertEqual(store.legal_email_contact, self.store_kwargs['legal_email_contact'])
        self.assertEqual(store.preferred_email_contact, self.store_kwargs['preferred_email_contact'])
        self.assertEqual(store.store_type, self.store_kwargs['store_type'])
        self.assertEqual(store.opening_date, self.store_kwargs['opening_date'])
        self.assertEqual(store.size, self.store_kwargs['size'])
        self.assertEqual(store.legal_nature, self.store_kwargs['legal_nature'])
        self.assertEqual(store.cnae_code, self.store_kwargs['cnae_code'])
        self.assertEqual(store.branch_classification, self.store_kwargs['branch_classification'])
        self.assertListEqual(store.images, self.store_kwargs['images'])

    def test_default_images_empty_list(self) -> None:
        kwargs = dict(self.store_kwargs)
        kwargs.pop('images')
        store = Store(**kwargs)
        self.assertEqual(store.images, [])
