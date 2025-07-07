from logging_config import setup_logging
setup_logging()

from middleware import log_requests_response
from dependencies import get_masker
from fastapi import FastAPI, Depends, HTTPException
from services import BaseMasker
from models.masking import MaskingRequest, MaskingResponse
from typing import List


app = FastAPI()
app.middleware("http")(log_requests_response)


@app.get("/")
async def root():
    return "Hello world!"


@app.post("/mask")
async def mask(
    masking_request: MaskingRequest,
    masker: BaseMasker = Depends(get_masker)
) -> List[MaskingResponse]:

    try:
        masking_responses: list[MaskingResponse] = []
        for text in masking_request.texts:
            masked_output = masker.mask(text)

            masking_responses.append(MaskingResponse(masked_text=masked_output.masked_text, mask_mapping=masked_output.mask_mapping))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return masking_responses
