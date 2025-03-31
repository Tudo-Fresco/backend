from sqlalchemy import Column, String, Date, Enum
from sqlalchemy.orm import relationship
from api.infrastructure.models.base_model import BaseModel
from api.enums.gender_type import GenderType


class UserModel(BaseModel):
    __tablename__ = 'user'

    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_picture = Column(String(256), nullable=True)

    password = Column(String(256), nullable=False)

    stores = relationship('StoreModel', back_populates='owner')
    demands = relationship('DemandModel', back_populates='responsible')
