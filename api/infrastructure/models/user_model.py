from typing import List
from sqlalchemy import Column, String, Date, Enum
from sqlalchemy.orm import relationship
from api.domain.entities.user import User
from api.infrastructure.models.base_model import BaseModel
from api.enums.gender_type import GenderType
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.models.store_model import StoreModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_picture = Column(String(256), nullable=True)

    password = Column(String(256), nullable=False)

    stores: List[StoreModel] = relationship('StoreModel', back_populates='owner')
    demands: List[DemandModel] = relationship('DemandModel', back_populates='responsible')

    def from_entity(self, entity: User) -> None:
        """Convert a User entity to the UserModel."""
        self.uuid = entity.uuid
        self.name = entity.name
        self.email = entity.email
        self.date_of_birth = entity.date_of_birth
        self.gender = entity.gender
        self.phone_number = entity.phone_number
        self.profile_picture = entity.profile_picture
        self.password = entity.password
        self.stores = entity.stores
        self.demands = entity.demands

    def to_entity(self) -> User:
        """Convert the UserModel to a User entity."""
        return User(
            uuid=self.uuid,
            name=self.name,
            email=self.email,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            phone_number=self.phone_number,
            profile_picture=self.profile_picture,
            password=self.password,
            stores=[store.to_entity() for store in self.stores],
            demands=[demand.to_entity() for demand in self.demands]
        )