import os

from Crypto.Cipher import AES


def aes_encrypt(key: bytes, data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=os.urandom(12))
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return b"".join([cipher.nonce, ciphertext, tag])


def aes_decrypt(key: bytes, data: bytes) -> bytes:
    nonce, tag = data[:12], data[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(data[12:-16], tag)
