from unittest.mock import MagicMock
from api.domain.store import Store
from api.domain.address import Address
from api.domain.group import Group
from api.domain.user import User
from api.enums.store_status import StoreStatus
from api.exceptions.validation_exception import ValidationException
import unittest


class TestStore(unittest.TestCase):
    
    def setUp(self) -> None:
        self.headquarters_mock = MagicMock(spec=Store)
        self.address_mock = MagicMock(spec=Address)
        self.group_mock = MagicMock(spec=Group)
        self.owner_mock = MagicMock(spec=User)
        self.store = Store(
            headquarters=self.headquarters_mock,
            image_urls=["http://example.com/image.jpg"],
            cnpj="12.345.678/0001-95",
            address=self.address_mock,
            status=StoreStatus.ACTIVE,
            reputation=4.5,
            trade_name="Loja Teste",
            legal_name="Loja Teste Ltda",
            group=self.group_mock,
            working_hours="09:00 - 18:00",
            owner=self.owner_mock
        )
    
    def test_validate_must_pass_for_all_properties(self) -> None:
        self.store.validate()
        self.address_mock.validate.assert_called_once()
        self.group_mock.validate.assert_called_once()
        self.owner_mock.validate.assert_called_once()
    
    def test_validate_must_raise_validation_exception_when_cnpj_is_invalid(self) -> None:
        self.store.cnpj = "invalid_cnpj"
        with self.assertRaises(ValidationException):
            self.store.validate()
    
    def test_validate_must_raise_validation_exception_when_reputation_is_negative(self) -> None:
        self.store.reputation = -1.0
        with self.assertRaises(ValidationException):
            self.store.validate()
    
    def test_validate_must_raise_validation_exception_when_reputation_is_greater_than_five(self) -> None:
        self.store.reputation = 5.1
        with self.assertRaises(ValidationException):
            self.store.validate()
    
    def test_validate_must_raise_validation_exception_when_trade_name_is_empty(self) -> None:
        self.store.trade_name = ""
        with self.assertRaises(ValidationException):
            self.store.validate()
    
    def test_validate_must_raise_validation_exception_when_legal_name_is_empty(self) -> None:
        self.store.legal_name = ""
        with self.assertRaises(ValidationException):
            self.store.validate()
    
    def test_validate_must_raise_validation_exception_when_working_hours_is_empty(self) -> None:
        self.store.working_hours = ""
        with self.assertRaises(ValidationException):
            self.store.validate()
