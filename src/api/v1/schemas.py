from pydantic import BaseModel, Field

import docs


class SecretOutputSchema(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description=docs.MESSAGE_DESCRIPTION,
    )
    model_config = {
        "json_schema_extra": {
            "example": {
              "message": "my_message",
            }
        }
    }


class GenerateInputSchema(SecretOutputSchema):
    secret_phrase: str = Field(
        ...,
        min_length=1,
        max_length=32,
        description=docs.SECRET_PHRASE_DESCRIPTION,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
              "message": "my_message",
              "secret_phrase": "my_secret_phrase",
            }
        }
    }


class GenerateOutputSchema(BaseModel):
    secret_key: str = Field(
        ...,
        min_length=1,
        max_length=36,
        description=docs.SECRET_KEY_DESCRIPTION,
    )

