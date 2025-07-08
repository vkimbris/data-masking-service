from logging_config import setup_logging
setup_logging()

from middleware import log_requests_response
from fastapi import FastAPI

from routers import masking, vocabs

app = FastAPI()
app.middleware("http")(log_requests_response)

app.include_router(masking.router)
app.include_router(vocabs.router)


@app.get("/")
async def root():
    return "Hello world!"



