from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from services import BaseVocabsService
from dependencies import get_vocabs_service


router = APIRouter(tags=["Vocabularies"])


@router.get("/vocabs/{vocab_name}")
async def get_vocabulary(
    vocab_name: str,
    vocabs_service: BaseVocabsService = Depends(get_vocabs_service),
) -> StreamingResponse:

    if not vocabs_service.vocab_exists(vocab_name):
        raise HTTPException(status_code=404, detail="Vocab file not found")

    try:
        body_stream = vocabs_service.get_vocab(vocab_name)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return StreamingResponse(body_stream, media_type="text/plain")

@router.put("/vocabs")
async def put_vocabulary(
    file: UploadFile = File(...)
) -> str:
    contents = await file.read()

    print(contents)

    return "OK!"