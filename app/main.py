from logging_config import setup_logging
setup_logging()

import logging
import json

from middleware import log_requests_response
from dependencies import get_masker
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from services import BaseMasker
from contextlib import asynccontextmanager
from models.masking import MaskingRequest, MaskingResponse, DeMaskingRequest, DeMaskingResponse


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
) -> MaskingResponse:

    try:
        masked_output = masker.mask(json.dumps(masking_request.input, ensure_ascii=False))

        return MaskingResponse(
            metadata=masked_output.mask_mapping,
            output=json.loads(masked_output.masked_text),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/demask")
async def demask(
    demasking_request: DeMaskingRequest,
    masker: BaseMasker = Depends(get_masker)
) -> DeMaskingResponse:

    try:
        output: dict[str, str] = {}

        for key, value in demasking_request.input.items():
            output[key] = masker.demask(value, demasking_request.metadata)

        return DeMaskingResponse(output=output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
