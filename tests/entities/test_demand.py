import unittest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from unittest.mock import Mock
from api.domain.entities.demand import Demand
from api.enums.demand_status import DemandStatus


class TestDemand(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_store = Mock()
        self.mock_product = Mock()
        self.mock_responsible = Mock()
        self.deadline = datetime.now(timezone.utc) + timedelta(days=7)

        self.demand = Demand(
            store=self.mock_store,
            product=self.mock_product,
            responsible=self.mock_responsible,
            needed_count=50,
            description="Urgent demand for product",
            deadline=self.deadline,
            status=DemandStatus.ANY,
            minimum_count=10,
            uuid=uuid4(),
            active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def test_initialization(self) -> None:
        self.assertIs(self.demand.store, self.mock_store)
        self.assertIs(self.demand.product, self.mock_product)
        self.assertIs(self.demand.responsible, self.mock_responsible)
        self.assertEqual(self.demand.needed_count, 50)
        self.assertEqual(self.demand.description, "Urgent demand for product")
        self.assertEqual(self.demand.deadline, self.deadline)
        self.assertEqual(self.demand.status, DemandStatus.ANY)
        self.assertEqual(self.demand.minimum_count, 10)

    def test_attributes_types(self) -> None:
        self.assertIsInstance(self.demand.needed_count, int)
        self.assertIsInstance(self.demand.description, str)
        self.assertIsInstance(self.demand.deadline, datetime)
        self.assertIsInstance(self.demand.status, DemandStatus)
        self.assertIsInstance(self.demand.minimum_count, int)
