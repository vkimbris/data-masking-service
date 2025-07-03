from fastapi import FastAPI, Depends

from services import BaseMasker
from models.masking import MaskingRequest, MaskingResponse

from dependencies import get_masker

from typing import List


app = FastAPI()


@app.get("/")
async def root():
    return "Hello world!"


@app.post("/mask")
async def mask(
    masking_request: MaskingRequest,
    masker: BaseMasker = Depends(get_masker)
) -> List[MaskingResponse]:

    masking_responses: list[MaskingResponse] = []
    for text in masking_request.texts:
        masked_output = masker.mask(text)

        masking_responses.append(MaskingResponse(masked_text=masked_output.masked_text, mask_mapping=masked_output.mask_mapping))

    return masking_responses
