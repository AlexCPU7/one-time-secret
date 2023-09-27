from unittest.mock import patch

import docs


async def test_api_v1_generate_405(client):
    response = await client.get("/api/v1/generate")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


async def test_api_v1_generate_422_case_1(client):
    response = await client.post("/api/v1/generate")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body"],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.3/v/missing"
            }
        ]
    }


async def test_api_v1_generate_case_2(client):
    response = await client.post("/api/v1/generate", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "message"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.3/v/missing"},
            {
                "type": "missing",
                "loc": ["body", "secret_phrase"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.3/v/missing"
            }
        ]
    }


@patch("api.v1.controllers.generate_secret_key")
async def test_api_v1_generate(mock_generate_secret_key, client):
    mock_secret_key = "mock_secret_key"
    mock_generate_secret_key.return_value = mock_secret_key
    response = await client.post(
        "/api/v1/generate",
        json={
            "message": "my_message",
            "secret_phrase": "my_secret_phrase",
        }
    )
    assert response.status_code == 200
    assert response.json() == {"secret_key": mock_secret_key}


@patch("api.v1.controllers.verify_secret_phrase")
async def test_api_v1_secrets_400(mock_verify_secret_phrase, client):
    mock_verify_secret_phrase.return_value = False
    response = await client.get(
        "/api/v1/secrets/mock_secret_key",
        params={"secret_phrase": "my_secret_phrase"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": docs.ERROR_400_SECRET}


@patch("api.v1.controllers.decrypt_message")
@patch("api.v1.controllers.verify_secret_phrase")
async def test_api_v1_secrets(mock_verify_secret_phrase, mock_decrypt_message, client):
    given = "mock_message"
    mock_verify_secret_phrase.return_value = True
    mock_decrypt_message.return_value = given
    response = await client.get(
        "/api/v1/secrets/mock_secret_key",
        params={"secret_phrase": "my_secret_phrase"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": given}
