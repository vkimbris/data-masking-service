from fastapi import APIRouter, Depends, HTTPException

from models.masking import MaskingRequest, MaskingResponse
from services import BaseMasker
from dependencies import get_masker

from typing import List


router = APIRouter(tags=["Masking"])


@router.post("/mask")
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

@router.post("/de_mask")
async def de_mask(
    masker: BaseMasker = Depends(get_masker)
) -> List[MaskingResponse]:
    pass
