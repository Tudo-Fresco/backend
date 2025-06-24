import unittest
from datetime import datetime, timezone
from uuid import UUID, uuid4
from api.domain.entities.address import Address


class TestAddress(unittest.TestCase):

    def setUp(self) -> None:
        self.uuid = uuid4()
        self.active = True
        self.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
        self.updated_at = datetime(2021, 1, 1, tzinfo=timezone.utc)
        self.address = Address(
            uuid=self.uuid,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            zip_code="12345-678",
            street_address="Main Street 123",
            latitude=12.3456,
            longitude=65.4321,
            province="SomeProvince",
            city="SomeCity",
            neighbourhood="Downtown",
            number="42B",
            additional_info="Near the park"
        )

    def test_initialization(self) -> None:
        self.assertEqual(self.address.zip_code, "12345-678")
        self.assertEqual(self.address.street_address, "Main Street 123")
        self.assertEqual(self.address.latitude, 12.3456)
        self.assertEqual(self.address.longitude, 65.4321)
        self.assertEqual(self.address.province, "SomeProvince")
        self.assertEqual(self.address.city, "SomeCity")
        self.assertEqual(self.address.neighbourhood, "Downtown")
        self.assertEqual(self.address.number, "42B")
        self.assertEqual(self.address.additional_info, "Near the park")
        self.assertEqual(self.address.uuid, self.uuid)
        self.assertEqual(self.address.active, self.active)
        self.assertEqual(self.address.created_at, self.created_at)
        self.assertEqual(self.address.updated_at, self.updated_at)

    def test_activate_and_deactivate(self) -> None:
        self.address.deactivate()
        self.assertFalse(self.address.active)
        self.address.activate()
        self.assertTrue(self.address.active)

    def test_update_timestamp(self) -> None:
        old_updated_at = self.address.updated_at
        self.address.update_timestamp()
        self.assertGreater(self.address.updated_at, old_updated_at)

    def test_update_method(self) -> None:
        self.address.some_field = "old"
        old_updated_at = self.address.updated_at
        self.address.update(
            some_field="new",
            zip_code="99999-999",
            uuid=uuid4(),
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
            active=False,
        )
        self.assertEqual(self.address.some_field, "new")
        self.assertEqual(self.address.zip_code, "99999-999")
        self.assertTrue(self.address.active)
        self.assertEqual(self.address.uuid, self.uuid)
        self.assertEqual(self.address.created_at, self.created_at)
        self.assertGreater(self.address.updated_at, old_updated_at)

    def test_to_dict_output(self) -> None:
        d = self.address.to_dict()
        self.assertIn('uuid', d)
        self.assertIn('created_at', d)
        self.assertIn('updated_at', d)
        self.assertEqual(d['zip_code'], "12345-678")
        self.assertEqual(d['street_address'], "Main Street 123")
        self.assertEqual(d['latitude'], 12.3456)
        self.assertEqual(d['longitude'], 65.4321)
        self.assertEqual(d['province'], "SomeProvince")
        self.assertEqual(d['city'], "SomeCity")
        self.assertEqual(d['neighbourhood'], "Downtown")
        self.assertEqual(d['number'], "42B")
        self.assertEqual(d['additional_info'], "Near the park")

    def test_set_base_properties(self) -> None:
        new_uuid = uuid4()
        new_created = datetime(1999, 12, 31, tzinfo=timezone.utc)
        new_updated = datetime(2000, 1, 1, tzinfo=timezone.utc)
        self.address.set_base_properties(new_uuid, False, new_created, new_updated)
        self.assertEqual(self.address.uuid, new_uuid)
        self.assertFalse(self.address.active)
        self.assertEqual(self.address.created_at, new_created)
        self.assertEqual(self.address.updated_at, new_updated)

    def test_enforce_uuid_accepts_string_and_uuid(self) -> None:
        string_uuid = str(uuid4())
        enforced_uuid1 = self.address._enforce_uuid(string_uuid)
        enforced_uuid2 = self.address._enforce_uuid(uuid4())
        self.assertIsInstance(enforced_uuid1, UUID)
        self.assertIsInstance(enforced_uuid2, UUID)

    def test_enforce_datetime_accepts_string_and_datetime(self) -> None:
        string_date = "2023-01-01T12:00:00+00:00"
        dt1 = self.address._enforce_datetime(string_date)
        dt2 = self.address._enforce_datetime(datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
        self.assertIsInstance(dt1, datetime)
        self.assertIsInstance(dt2, datetime)
        self.assertEqual(dt1, datetime.fromisoformat(string_date))
        self.assertEqual(dt2, datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc))

