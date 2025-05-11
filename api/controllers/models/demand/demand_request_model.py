from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field
from api.controllers.models.base_request_model import BaseRequestModel
from api.enums.demand_status import DemandStatus


class DemandRequestModel(BaseRequestModel):
    store_uuid: UUID = Field(..., example='1f4e1f4b-ea47-4d3c-8901-cdcd7bb8e10a')
    product_uuid: UUID = Field(..., example='2d7f5e9f-fb71-4fd2-b929-2d6d7a99fa7a')
    responsible_uuid: Optional[UUID] = Field(example='3f8d2f7e-3a14-44db-8f69-093eb8f123b1', default=None)
    needed_count: int = Field(..., example=50)
    description: str = Field(..., example='50 packs of organic rice')
    deadline: datetime = Field(..., example='2025-10-01T12:00:00')
    status: DemandStatus = Field(..., example=DemandStatus.OPENED.value)

