from api.infrastructure.models.base_model import BaseModel
from sqlalchemy import Column, String, Float


class AddressModel(BaseModel):
    __tablename__ = 'address'

    zip_code = Column(String(20), nullable=False)
    street_address = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    neighbourhood = Column(String(100), nullable=False)
    number = Column(String(20), nullable=False)
    additional_info = Column(String(256), nullable=False, server_default='')
