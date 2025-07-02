from dotenv import load_dotenv

from services import PresidioMasker

load_dotenv()

import os

from functools import lru_cache
from services import BaseMasker


@lru_cache()
def get_masker() -> BaseMasker:
    masker_type = os.getenv("MASKER_TYPE")

    if masker_type is None:
        raise ValueError("MASKER_TYPE environment variable is not set")

    if masker_type == "presidio":
        masker = PresidioMasker(path_to_config=os.getenv("MASKER_CONFIG_PATH"))

    else:
        raise ValueError("There is no implementation for {}")

    return masker