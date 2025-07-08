from logging_config import setup_logging
setup_logging()

import logging

from middleware import log_requests_response
from dependencies import get_masker
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from services import BaseMasker
from contextlib import asynccontextmanager
from models.masking import MaskingRequest, MaskingResponse, DeMaskingRequest, DeMaskingResponse
from typing import List


logger = logging.getLogger("custom-logger")

@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        logger.info("Waiting for application startup")

        logger.info("Application startup complete.")
        yield

    except Exception as e:
        logger.error(f"Error! Message: {str(e)}")


app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_requests_response)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception in {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )


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

@app.post("/de_mask")
async def de_mask(
    de_masking_request: DeMaskingRequest,
    masker: BaseMasker = Depends(get_masker)
) -> DeMaskingResponse:

    try:
        de_masked_texts: list[str] = []

        for inp in de_masking_request.inputs:
            de_masked_text = masker.de_mask(text=inp.masked_text, entities=inp.mask_mapping)

            de_masked_texts.append(de_masked_text)

        return DeMaskingResponse(de_masked_texts=de_masked_texts)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
