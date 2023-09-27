from unittest.mock import Mock, AsyncMock, patch

import pytest
from fastapi import HTTPException

import docs
from api.v1.controllers import generate_secret_key, create_and_get_secret_key, read_and_delete_secret_key
from api.v1.schemas import GenerateInputSchema


def test_generate_secret_key():
    result = generate_secret_key()
    assert type(result) is str
    assert len(result) == 36


@patch("api.v1.controllers.generate_secret_key", lambda: "mock_secret_key")
async def test_create_and_get_secret_key():
    schema = GenerateInputSchema(message="my_message", secret_phrase="my_secret_phrase")
    result = await create_and_get_secret_key(schema, AsyncMock())
    assert result == "mock_secret_key"


async def test_read_and_delete_secret_key_error_404():
    with pytest.raises(HTTPException) as info_error:
        session = AsyncMock()
        session.execute.return_value = Mock(one_or_none=lambda: False)
        await read_and_delete_secret_key("mock_secret_key", "mock_secret_phrase", session)
    assert info_error.value.status_code == 404
    assert info_error.value.detail == docs.ERROR_404_SECRET


@patch("api.v1.controllers.verify_secret_phrase")
async def test_read_and_delete_secret_key_error_400(mock_verify_secret_phrase):
    with pytest.raises(HTTPException) as info_error:
        mock_verify_secret_phrase.return_value = False
        session = AsyncMock()
        session.execute.return_value = Mock(one_or_none=lambda: Mock())
        await read_and_delete_secret_key("mock_secret_key", "mock_secret_phrase", session)
    assert info_error.value.status_code == 400
    assert info_error.value.detail == docs.ERROR_400_SECRET


@patch("api.v1.controllers.decrypt_message")
@patch("api.v1.controllers.verify_secret_phrase")
async def test_read_and_delete_secret_key(mock_verify_secret_phrase, mock_decrypt_message):
    given = "mock_message"
    mock_verify_secret_phrase.return_value = True
    mock_decrypt_message.return_value = given
    session = AsyncMock()
    session.execute.return_value = Mock(one_or_none=lambda: Mock())
    result = await read_and_delete_secret_key(
        "mock_secret_key",
        "mock_secret_phrase",
        session
    )
    assert result == given
