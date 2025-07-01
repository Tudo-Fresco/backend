from sqlalchemy import Column, String, Float
from api.infrastructure.models.base_model import BaseModel
from api.domain.entities.address import Address


class AddressModel(BaseModel):
    __tablename__ = 'address'

    zip_code = Column(String(32), nullable=False)
    street_address = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    neighbourhood = Column(String(100), nullable=False)
    number = Column(String(32), nullable=False)
    additional_info = Column(String(256), nullable=False, default='')

    def _from_entity(self, entity: Address) -> None:
        '''Convert an Address entity to the AddressModel.'''
        self.zip_code = entity.zip_code
        self.street_address = entity.street_address
        self.latitude = entity.latitude
        self.longitude = entity.longitude
        self.province = entity.province
        self.city = entity.city
        self.neighbourhood = entity.neighbourhood
        self.number = entity.number
        self.additional_info = entity.additional_info

    def _to_entity(self) -> Address:
        '''Convert the AddressModel to an Address entity.'''
        return Address(
            zip_code=self.zip_code,
            street_address=self.street_address,
            latitude=self.latitude,
            longitude=self.longitude,
            province=self.province,
            city=self.city,
            neighbourhood=self.neighbourhood,
            number=self.number,
            additional_info=self.additional_info
        )