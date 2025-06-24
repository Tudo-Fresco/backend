import unittest
from unittest.mock import MagicMock
from datetime import date
from api.infrastructure.models.store_model import StoreModel
from api.domain.entities.store import Store
from api.enums.store_type import StoreType

class TestStoreModel(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_address = MagicMock()
        self.mock_address.uuid = 'address-uuid-mock'
        self.mock_address.to_entity = MagicMock(return_value='address-entity-mock')
        self.mock_owner = MagicMock()
        self.mock_owner.uuid = 'owner-uuid-mock'
        self.mock_owner.to_entity = MagicMock(return_value='owner-entity-mock')
        self.store_entity = Store(
            images=['img1.png', 'img2.png'],
            cnpj='12.345.678/0001-99',
            address=self.mock_address,
            reputation=4.5,
            trade_name='Trade Name',
            legal_name='Legal Name Ltda',
            owner=self.mock_owner,
            legal_phone_contact='+5511999999999',
            preferred_phone_contact='+5511888888888',
            legal_email_contact='legal@example.com',
            preferred_email_contact='preferred@example.com',
            store_type=StoreType.RETAILER,
            opening_date=date(2020, 1, 1),
            size='Medium',
            legal_nature='Nature',
            cnae_code='1234',
            branch_classification='Classification'
        )

    def test_from_entity_populates_model_fields(self) -> None:
        model = StoreModel()
        model._from_entity(self.store_entity)
        self.assertEqual(model.images, self.store_entity.images)
        self.assertEqual(model.cnpj, self.store_entity.cnpj)
        self.assertEqual(model.address_uuid, self.mock_address.uuid)
        self.assertEqual(model.reputation, self.store_entity.reputation)
        self.assertEqual(model.trade_name, self.store_entity.trade_name)
        self.assertEqual(model.legal_name, self.store_entity.legal_name)
        self.assertEqual(model.owner_uuid, self.mock_owner.uuid)
        self.assertEqual(model.legal_phone_contact, self.store_entity.legal_phone_contact)
        self.assertEqual(model.preferred_phone_contact, self.store_entity.preferred_phone_contact)
        self.assertEqual(model.legal_email_contact, self.store_entity.legal_email_contact)
        self.assertEqual(model.preferred_email_contact, self.store_entity.preferred_email_contact)
        self.assertEqual(model.store_type, self.store_entity.store_type)
        self.assertEqual(model.opening_date, self.store_entity.opening_date)
        self.assertEqual(model.size, self.store_entity.size)
        self.assertEqual(model.legal_nature, self.store_entity.legal_nature)
        self.assertEqual(model.cnae_code, self.store_entity.cnae_code)
        self.assertEqual(model.branch_classification, self.store_entity.branch_classification)

    def test_to_entity_returns_store_with_correct_fields(self) -> None:
        model = StoreModel()
        model.images = ['img1.png', 'img2.png']
        model.cnpj = '12.345.678/0001-99'
        model.address = MagicMock()
        model.address.to_entity = MagicMock(return_value=self.mock_address)
        model.reputation = 4.5
        model.trade_name = 'Trade Name'
        model.legal_name = 'Legal Name Ltda'
        model.owner = MagicMock()
        model.owner.to_entity = MagicMock(return_value=self.mock_owner)
        model.legal_phone_contact = '+5511999999999'
        model.preferred_phone_contact = '+5511888888888'
        model.legal_email_contact = 'legal@example.com'
        model.preferred_email_contact = 'preferred@example.com'
        model.store_type = StoreType.RETAILER
        model.opening_date = date(2020, 1, 1)
        model.size = 'Medium'
        model.legal_nature = 'Nature'
        model.cnae_code = '1234'
        model.branch_classification = 'Classification'
        entity = model._to_entity()
        self.assertEqual(entity.images, model.images)
        self.assertEqual(entity.cnpj, model.cnpj)
        self.assertEqual(entity.address, self.mock_address)
        self.assertEqual(entity.reputation, model.reputation)
        self.assertEqual(entity.trade_name, model.trade_name)
        self.assertEqual(entity.legal_name, model.legal_name)
        self.assertEqual(entity.owner, self.mock_owner)
        self.assertEqual(entity.legal_phone_contact, model.legal_phone_contact)
        self.assertEqual(entity.preferred_phone_contact, model.preferred_phone_contact)
        self.assertEqual(entity.legal_email_contact, model.legal_email_contact)
        self.assertEqual(entity.preferred_email_contact, model.preferred_email_contact)
        self.assertEqual(entity.store_type, model.store_type)
        self.assertEqual(entity.opening_date, model.opening_date)
        self.assertEqual(entity.size, model.size)
        self.assertEqual(entity.legal_nature, model.legal_nature)
        self.assertEqual(entity.cnae_code, model.cnae_code)
        self.assertEqual(entity.branch_classification, model.branch_classification)