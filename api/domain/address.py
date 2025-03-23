from api.domain.base_entity import BaseEntity


class Address(BaseEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)