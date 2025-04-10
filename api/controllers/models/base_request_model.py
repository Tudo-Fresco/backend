from typing import Any
from pydantic import BaseModel

class BaseRequestModel(BaseModel):
    class Config:
        @staticmethod
        def schema_extra(schema: dict[str, Any], model_class: type) -> None:
            schema.clear()