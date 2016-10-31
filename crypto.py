from Crypto.Cipher import AES
from hashlib import sha256
from base64 import b64encode

def create_key(string):
    hashed = sha256(bytes(string, 'utf8')).digest()
    return hashed

def encrypt(message, key):
    AESchiper = AES.new(key)
    # length of a message must be multiple of 16
    return AESchiper.encrypt(message)

def decrypt(message, key):
    AESchiper = AES.new(key)
    return AESchiper.decrypt(message)
