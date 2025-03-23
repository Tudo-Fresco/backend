from api.domain.base_entity import BaseEntity


class User(BaseEntity):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)