from hash import hash_secret_phrase, verify_secret_phrase, encrypt_message, decrypt_message


def test_hash_secret_phrase(secret_phrase_origin, secret_phrase_hash):
    assert hash_secret_phrase(secret_phrase_origin) == secret_phrase_hash


def test_verify_secret_phrase_true(secret_phrase_origin, secret_phrase_hash):
    assert verify_secret_phrase(secret_phrase_origin, secret_phrase_hash) is True


def test_verify_secret_phrase_false_case_1(secret_phrase_origin):
    assert verify_secret_phrase(secret_phrase_origin, "test") is False


def test_verify_secret_phrase_false_case_2(secret_phrase_hash):
    assert verify_secret_phrase("test", secret_phrase_hash) is False


def test_encrypt_message():
    message = "My message"
    message_hash = encrypt_message(message)
    result = decrypt_message(message_hash)
    assert result == message
