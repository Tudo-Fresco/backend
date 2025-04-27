from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class BaseResponseModel(BaseModel):
    uuid: Optional[str] = Field(None, example='123e4567-e89b-12d3-a456-426614174000')
    created_at: Optional[str] = Field(None, example='2025-04-27T00:00:00Z')
    updated_at: Optional[str] = Field(None, example='2025-04-27T00:00:00Z')