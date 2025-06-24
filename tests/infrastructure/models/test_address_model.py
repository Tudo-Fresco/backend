import unittest
from uuid import uuid4
from datetime import datetime, timezone
from api.infrastructure.models.address_model import AddressModel
from api.domain.entities.address import Address


class TestAddressModel(unittest.TestCase):

    def make_address_entity(self) -> Address:
        return Address(
            uuid=uuid4(),
            active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            zip_code="12345-678",
            street_address="Main St 123",
            latitude=12.3456,
            longitude=65.4321,
            province="ProvinceX",
            city="CityY",
            neighbourhood="NeighborhoodZ",
            number="42B",
            additional_info="Near the park"
        )

    def test_from_entity_populates_model_fields(self) -> None:
        entity = self.make_address_entity()
        model = AddressModel()
        model.from_entity(entity)
        self.assertEqual(model.uuid, entity.uuid)
        self.assertEqual(model.active, entity.active)
        self.assertEqual(model.created_at, entity.created_at)
        self.assertEqual(model.updated_at, entity.updated_at)
        self.assertEqual(model.zip_code, entity.zip_code)
        self.assertEqual(model.street_address, entity.street_address)
        self.assertEqual(model.latitude, entity.latitude)
        self.assertEqual(model.longitude, entity.longitude)
        self.assertEqual(model.province, entity.province)
        self.assertEqual(model.city, entity.city)
        self.assertEqual(model.neighbourhood, entity.neighbourhood)
        self.assertEqual(model.number, entity.number)
        self.assertEqual(model.additional_info, entity.additional_info)

    def test_to_entity_returns_address_with_correct_fields(self) -> None:
        model = AddressModel()
        model.uuid = uuid4()
        model.active = True
        now = datetime.now(timezone.utc)
        model.created_at = now
        model.updated_at = now
        model.zip_code = "54321-987"
        model.street_address = "Second St 456"
        model.latitude = 98.7654
        model.longitude = 43.2109
        model.province = "ProvinceA"
        model.city = "CityB"
        model.neighbourhood = "NeighborhoodC"
        model.number = "101"
        model.additional_info = "Opposite to school"
        entity = model.to_entity()
        self.assertEqual(entity.uuid, model.uuid)
        self.assertEqual(entity.active, model.active)
        self.assertEqual(entity.created_at, model.created_at)
        self.assertEqual(entity.updated_at, model.updated_at)
        self.assertEqual(entity.zip_code, model.zip_code)
        self.assertEqual(entity.street_address, model.street_address)
        self.assertEqual(entity.latitude, model.latitude)
        self.assertEqual(entity.longitude, model.longitude)
        self.assertEqual(entity.province, model.province)
        self.assertEqual(entity.city, model.city)
        self.assertEqual(entity.neighbourhood, model.neighbourhood)
        self.assertEqual(entity.number, model.number)
        self.assertEqual(entity.additional_info, model.additional_info)