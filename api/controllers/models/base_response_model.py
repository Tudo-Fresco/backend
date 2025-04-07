from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class BaseResponseModel(BaseModel):
    id: UUID = Field(..., example='de305d54-75b4-431b-adb2-eb6b9e546014')
    created_at: datetime = Field(..., example='2024-01-01T12:00:00Z')
    updated_at: datetime = Field(..., example='2024-01-01T12:30:00Z')
