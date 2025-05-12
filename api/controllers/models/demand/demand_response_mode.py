from datetime import datetime
from pydantic import Field
from api.controllers.models.base_response_model import BaseResponseModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus


class DemandResponseModel(BaseResponseModel):
    store: StoreResponseModel = Field(..., example={})
    product: ProductResponseModel = Field(..., example={})
    responsible: UserResponseModel = Field(..., example={})
    needed_count: int = Field(..., example=50)
    description: str = Field(..., example='Arroz orgânico da instância Canela Preta')
    deadline: datetime = Field(..., example='2025-10-01T12:00:00')
    status: DemandStatus = Field(..., example=DemandStatus.OPENED.value)
    minimum_count: int = Field(..., example=777)