from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

import docs
from api.v1.schemas import GenerateInputSchema
from hash import hash_secret_phrase, verify_secret_phrase, encrypt_message, decrypt_message
from models.secret import Secret


def generate_secret_key() -> str:
    return str(uuid4())


async def create_and_get_secret_key(schema: GenerateInputSchema, session: AsyncSession) -> str:
    data = {
        "secret_key": generate_secret_key(),
        "hash_secret_phrase": hash_secret_phrase(schema.secret_phrase),
        "hash_message": encrypt_message(schema.message),
    }
    await session.execute(
        insert(
            Secret
        ).values(
            **data
        )
    )
    await session.commit()
    return data["secret_key"]


async def read_and_delete_secret_key(secret_key: str, secret_phrase: str, session: AsyncSession) -> str:
    secret_row = await session.execute(
        select(
            Secret.hash_message,
            Secret.hash_secret_phrase,
        ).where(
            Secret.secret_key == secret_key,
        )
    )
    secret = secret_row.one_or_none()
    if not secret:
        raise HTTPException(status_code=404, detail=docs.ERROR_404_SECRET)

    if not verify_secret_phrase(secret_phrase, secret.hash_secret_phrase):
        raise HTTPException(status_code=400, detail=docs.ERROR_400_SECRET)

    await session.execute(
        delete(
            Secret
        ).where(
            Secret.hash_message == secret.hash_message
        )
    )
    await session.commit()

    return decrypt_message(secret.hash_message)
