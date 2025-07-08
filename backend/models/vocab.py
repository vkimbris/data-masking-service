from pydantic import BaseModel
from typing import List


class Vocabulary(BaseModel):
    values: List[str]