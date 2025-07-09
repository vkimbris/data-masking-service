from pydantic import BaseModel
from typing import Dict, List, Any


class MaskingRequest(BaseModel):
    input: Dict[str, str]


class MaskingResponse(BaseModel):
    metadata: Dict[str, str]
    output: Dict[str, str]


class DeMaskingRequest(BaseModel):
    metadata: Dict[str, str]
    input: Dict[str, str]


class DeMaskingResponse(BaseModel):
    output: Dict[str, str]
