import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from api.domain.entities.address import Address
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.repositories.address_repository import AddressRepository

class TestAddressRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_session = AsyncMock()
        self.repo = AddressRepository(self.mock_session)

    def test_init_sets_attributes(self):
        self.assertEqual(self.repo.session, self.mock_session)
        self.assertEqual(self.repo.model_class, AddressModel)
        self.assertTrue(hasattr(self.repo, 'logger'))
        self.assertIn('AddressRepository', self.repo.logger.who)

    @pytest.mark.asyncio
    async def test_create_calls_session_add_and_commit(self) -> None:
        address = MagicMock(spec=Address)
        address.zip_code = '12345-678'
        address.street_address = 'Some street'
        address.latitude = 10.0
        address.longitude = 20.0
        address.province = 'Some province'
        address.city = 'Some city'
        address.neighbourhood = 'Some neighbourhood'
        address.number = '123'
        address.additional_info = 'info'
        address.uuid = uuid4()
        address.active = True
        address.created_at = None
        address.updated_at = None
        with patch.object(AddressModel, 'from_entity', autospec=True) as mock_from_entity:
            mock_session = MagicMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            repo = AddressRepository(mock_session)
            await repo.create(address)
            assert mock_session.add.call_count == 1
            assert mock_session.commit.await_count == 1
            mock_from_entity.assert_called_once()
            called_model_instance = mock_from_entity.call_args[0][0]
            called_address = mock_from_entity.call_args[0][1]
            assert isinstance(called_model_instance, AddressModel)
            assert called_address == address

    async def test_get_returns_entity_if_found(self) -> None:
        obj_id = uuid4()
        model_instance = MagicMock()
        model_instance.to_entity.return_value = 'entity'
        result = MagicMock()
        result.scalars.return_value.one_or_none.return_value = model_instance
        self.mock_session.execute.return_value = result

        entity = await self.repo.get(obj_id)
        self.assertEqual(entity, 'entity')
        self.mock_session.execute.assert_awaited_once()

    async def test_get_raises_not_found_when_none(self) -> None:
        obj_id = uuid4()
        result = MagicMock()
        result.scalars.return_value.one_or_none.return_value = None
        self.mock_session.execute.return_value = result
        with self.assertRaises(Exception) as context:
            await self.repo.get(obj_id)
        self.assertIn('Nenhum registro', str(context.exception))

    async def test_list_returns_entities(self):
        model1 = MagicMock()
        model1.to_entity.return_value = 'entity1'
        model2 = MagicMock()
        model2.to_entity.return_value = 'entity2'
        result = MagicMock()
        result.scalars.return_value.all.return_value = [model1, model2]
        self.mock_session.execute.return_value = result
        entities = await self.repo.list(page=1, per_page=10)
        self.assertEqual(entities, ['entity1', 'entity2'])
        self.mock_session.execute.assert_awaited_once()

    async def test_update_calls_merge_and_commit(self) -> None:
        address = MagicMock(spec=Address)
        address.uuid = uuid4()
        address.zip_code = '12345-678'
        address.street_address = 'Some street'
        address.latitude = 10.0
        address.longitude = 20.0
        address.province = 'Some province'
        address.city = 'Some city'
        address.neighbourhood = 'Some neighbourhood'
        address.number = '123'
        address.additional_info = 'info'
        self.repo.get = AsyncMock(return_value=address)
        with patch('api.infrastructure.models.address_model.AddressModel.from_entity', autospec=True) as mock_from_entity:
            await self.repo.update(address)
            mock_from_entity.assert_called_once()
            args, _ = mock_from_entity.call_args
            assert args[1] == address