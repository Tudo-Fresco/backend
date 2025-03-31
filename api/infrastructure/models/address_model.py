from api.domain.entities.address import Address
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

    def from_entity(self, entity: Address) -> None:
        """Converts a domain Address entity to the SQLAlchemy AddressModel."""
        self.zip_code = entity.zip_code
        self.street_address = entity.street_address
        self.latitude = entity.latitude
        self.longitude = entity.longitude
        self.province = entity.province
        self.city = entity.city
        self.neighbourhood = entity.neighbourhood
        self.number = entity.number
        self.additional_info = entity.additional_info
        self.uuid = entity.uuid
        self.active = entity.active
        self.created_at = entity.created_at
        self.updated_at = entity.updated_at
    
    def to_entity(self) -> Address:
        return Address(
            uuid=self.uuid,
            zip_code=self.zip_code,
            street_address=self.street_address,
            latitude=self.latitude,
            longitude=self.longitude,
            province=self.province,
            city=self.city,
            neighbourhood=self.neighbourhood,
            number=self.number,
            additional_info=self.additional_info,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )