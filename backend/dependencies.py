from dotenv import load_dotenv
load_dotenv()

import os

from services import BaseVocabsService, S3VocabsService
from services import PresidioMasker, BaseMasker

from functools import lru_cache


@lru_cache()
def get_masker() -> BaseMasker:
    masker_type = os.getenv("MASKER_TYPE")

    if masker_type is None:
        raise ValueError("MASKER_TYPE environment variable is not set")

    if masker_type == "presidio":
        masker = PresidioMasker(path_to_config=os.getenv("MASKER_CONFIG_PATH"))

    else:
        raise ValueError(f"There is no implementation for {masker_type}")

    return masker

@lru_cache()
def get_vocabs_service() -> BaseVocabsService:
    vocabs_service_type = os.getenv("VOCABS_SERVICE_TYPE")

    if vocabs_service_type is None:
        raise ValueError("VOCABS_SERVICE_TYPE environment variable is not set")

    if vocabs_service_type == "s3":
        vocabs_service = S3VocabsService(
            access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("AWS_ENDPOINTURL"),
            bucket_name=os.getenv("AWS_BUCKET_NAME"),
        )
    else:
        raise ValueError(f"There is no implementation for {vocabs_service_type}")

    return vocabs_service