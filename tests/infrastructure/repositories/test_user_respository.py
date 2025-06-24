import unittest
from unittest.mock import AsyncMock, MagicMock
from api.domain.entities.user import User
from api.infrastructure.models.user_model import UserModel
from api.infrastructure.repositories.user_repository import UserRepository
from api.exceptions.not_found_exception import NotFoundException


class TestUserRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock()
        self.repo = UserRepository(self.session)

    def make_user_model(self) -> MagicMock:
        model = MagicMock(spec=UserModel)
        model.to_entity.return_value = MagicMock(spec=User)
        return model

    async def test_get_by_email_returns_user_when_found(self) -> None:
        model = self.make_user_model()
        result_mock = MagicMock()
        result_mock.scalars().one_or_none.return_value = model
        self.session.execute.return_value = result_mock
        user = await self.repo.get_by_email("test@example.com")
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(user, User)
        model.to_entity.assert_called_once()

    async def test_get_by_email_raises_not_found_when_missing(self) -> None:
        result_mock = MagicMock()
        result_mock.scalars().one_or_none.return_value = None
        self.session.execute.return_value = result_mock
        with self.assertRaises(NotFoundException):
            await self.repo.get_by_email("missing@example.com")
