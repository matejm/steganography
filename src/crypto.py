from Crypto.Cipher import AES
from hashlib import sha256
from base64 import b64encode

def create_key(string):
    """
    Creates sha256 hash key from given string. Key is of the right length for AES encryption.

    :param string: String encoded with UTF-8.
    :returns: String key, a hash of ``string``.
    """
    hashed = sha256(bytes(string, 'utf8')).digest()
    return hashed

def encrypt(message, key):
    """
    Encrypts message with key, using AES encryption.

    :param message: Bytes object. Length must be multiple of 16.
    :param key: Key of length 16. Please use :func:`crypto.create_key` on your string.
    :returns: Encrypted message.
    """
    AESchiper = AES.new(key)
    # length of a message must be multiple of 16
    return AESchiper.encrypt(message)

def decrypt(message, key):
    """
    Decypts message with key, using AES encryption.

    :param message: Bytes object. Length must be multiple of 16.
    :param key: Key of length 16. Please use :func:`crypto.create_key` on your string.
    :returns: Decypted message.
    """
    AESchiper = AES.new(key)
    return AESchiper.decrypt(message)
