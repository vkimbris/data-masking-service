from pydantic import BaseModel
from typing import Dict, List


class MaskingRequest(BaseModel):
    texts: List[str]


class MaskingResponse(BaseModel):
    masked_text: str
    mask_mapping: Dict[str, str]
