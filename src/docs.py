MESSAGE_DESCRIPTION = "The secret message must be mandatory"
SECRET_PHRASE_DESCRIPTION = "The secret word must be binding"
SECRET_KEY_DESCRIPTION = ("The secret key is generated automatically, you need to paste it into the url "
                          "/secrets/{secret_key} and enter the secret phrase to display the secret message.")

ERROR_400_SECRET = "Incorrect secret phrase"
ERROR_404_SECRET = "You have entered incorrect data or this record does not exist"
ERROR_429_SECRET = "Rate limit exceeded: 600 per 1 minute"

MAIN_RESPONSES = {
    429: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Not Found",
                        "value": {"error": ERROR_429_SECRET}
                    },
                }
            }
        }
    },
}
GENERATE_RESPONSES = {
    **MAIN_RESPONSES,
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Success",
                        "value": {"secret_key": "151e4280-f4ed-4b2f-a96a-d0e2c7ed18c9"}
                    },
                }
            }
        }
    },
}
SECRETS_RESPONSES = {
    **MAIN_RESPONSES,
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Success",
                        "value": {"secret_key": "151e4280-f4ed-4b2f-a96a-d0e2c7ed18c9"}
                    },
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Bad Request",
                        "value": {"detail": ERROR_400_SECRET}
                    },
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Not Found",
                        "value": {"detail": ERROR_404_SECRET}
                    },
                }
            }
        }
    },
}
