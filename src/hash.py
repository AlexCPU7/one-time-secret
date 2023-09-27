from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad

from config import KEY_HASH


def hash_secret_phrase(secret_phrase: str) -> str:
    hash_object = SHA3_256.new(secret_phrase.encode())
    return hash_object.hexdigest()


def verify_secret_phrase(secret_phrase: str, hashed_secret_phrase: str) -> bool:
    hash_object = SHA3_256.new(secret_phrase.encode())
    hashed_input_secret_phrase = hash_object.hexdigest()
    return hashed_input_secret_phrase == hashed_secret_phrase


def encrypt_message(message: str) -> str:
    cipher = AES.new(KEY_HASH, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    encrypted_text = cipher.iv + ciphertext
    return encrypted_text.hex()


def decrypt_message(message_row: str) -> str:
    ciphertext = bytes.fromhex(message_row)
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(KEY_HASH, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
