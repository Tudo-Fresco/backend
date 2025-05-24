from typing import Optional
from pydantic import Field
from pydantic import BaseModel

class CoordinatesResponseModel(BaseModel):
    latitude: Optional[float] = Field(..., example=-23.561684)
    longitude: Optional[float] = Field(..., example=-46.655981)
