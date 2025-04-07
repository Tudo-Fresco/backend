from api.domain.entities.base_entity import BaseEntity


class Address(BaseEntity):

    def __init__(self, zip_code: str,
                street_address: str,
                latitude: float,
                longitude: float,
                province: str,
                city: str,
                neighbourhood: str,
                number: str,
                additional_info: str = '',
                **kwargs):
        super().__init__(**kwargs)
        self.zip_code: str = zip_code
        self.street_address: str = street_address
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.province: str = province
        self.city: str = city
        self.neighbourhood: str = neighbourhood
        self.number: str = number
        self.additional_info: str = additional_info