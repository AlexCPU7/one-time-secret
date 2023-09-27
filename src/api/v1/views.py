from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

import docs
from api.v1.controllers import create_and_get_secret_key, read_and_delete_secret_key
from api.v1.schemas import GenerateInputSchema, GenerateOutputSchema, SecretOutputSchema
from database import get_async_session

api_v1_router = APIRouter()


@api_v1_router.post(
    "/generate",
    tags=["api_v1"],
    response_model=GenerateOutputSchema,
    responses=docs.GENERATE_RESPONSES,
)
async def generate(
        schema: GenerateInputSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    The method is responsible for saving a secret message with a secret word. After saving, the secret key is issued.
    """
    secret_key = await create_and_get_secret_key(schema, session)
    return {"secret_key": secret_key}


@api_v1_router.get(
    "/secrets/{secret_key}",
    tags=["api_v1"],
    response_model=SecretOutputSchema,
    responses=docs.SECRETS_RESPONSES,
)
async def secrets(
        secret_key: str = Path(..., min_length=1, max_length=36, description=docs.SECRET_KEY_DESCRIPTION),
        secret_phrase: str = Query(..., min_length=1, max_length=32, description=docs.SECRET_PHRASE_DESCRIPTION),
        session: AsyncSession = Depends(get_async_session),
):
    """
    The method is responsible for one-time viewing of a secret message.\n
    To view the secret message you should enter the secret word.\n
    After viewing the secret message is deleted from the system without possibility to restore it.
    """
    message = await read_and_delete_secret_key(secret_key, secret_phrase, session)
    return {"message": message}
