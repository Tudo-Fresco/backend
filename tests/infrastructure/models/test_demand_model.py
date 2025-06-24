import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from api.infrastructure.models.demand_model import DemandModel
from api.domain.entities.demand import Demand
from api.domain.entities.store import Store
from api.domain.entities.product import Product
from api.domain.entities.user import User
from api.enums.demand_status import DemandStatus


class TestDemandModel(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_store = MagicMock(spec=Store)
        self.mock_store.uuid = uuid4()
        self.mock_product = MagicMock(spec=Product)
        self.mock_product.uuid = uuid4()
        self.mock_responsible = MagicMock(spec=User)
        self.mock_responsible.uuid = uuid4()
        self.entity = Demand(
            store=self.mock_store,
            product=self.mock_product,
            responsible=self.mock_responsible,
            needed_count=5,
            description="Test demand",
            deadline=datetime.now(timezone.utc),
            status=DemandStatus.OPENED,
            minimum_count=2
        )
        self.mock_store_model = MagicMock()
        self.mock_store_model.to_entity.return_value = self.mock_store
        self.mock_product_model = MagicMock()
        self.mock_product_model.to_entity.return_value = self.mock_product
        self.mock_responsible_model = MagicMock()
        self.mock_responsible_model.to_entity.return_value = self.mock_responsible

    def test_from_entity_populates_model_fields(self) -> None:
        model = DemandModel()
        model.from_entity(self.entity)
        self.assertEqual(model.store_uuid, self.entity.store.uuid)
        self.assertEqual(model.product_uuid, self.entity.product.uuid)
        self.assertEqual(model.responsible_uuid, self.entity.responsible.uuid)
        self.assertEqual(model.needed_count, self.entity.needed_count)
        self.assertEqual(model.description, self.entity.description)
        self.assertEqual(model.deadline, self.entity.deadline)
        self.assertEqual(model.status, self.entity.status)
        self.assertEqual(model.minimum_count, self.entity.minimum_count)

    def test_to_entity_returns_demand_with_correct_fields(self) -> None:
        model = DemandModel()
        model.store = self.mock_store_model
        model.product = self.mock_product_model
        model.responsible = self.mock_responsible_model
        model.needed_count = 10
        model.description = "Demand description"
        model.deadline = datetime.now(timezone.utc)
        model.status = DemandStatus.CLOSED
        model.minimum_count = 1
        demand_entity = model.to_entity()
        self.assertEqual(demand_entity.store, self.mock_store)
        self.assertEqual(demand_entity.product, self.mock_product)
        self.assertEqual(demand_entity.responsible, self.mock_responsible)
        self.assertEqual(demand_entity.needed_count, model.needed_count)
        self.assertEqual(demand_entity.description, model.description)
        self.assertEqual(demand_entity.deadline, model.deadline)
        self.assertEqual(demand_entity.status, model.status)
        self.assertEqual(demand_entity.minimum_count, model.minimum_count)