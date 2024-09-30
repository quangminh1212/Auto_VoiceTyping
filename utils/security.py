import os
from cryptography.fernet import Fernet

class Security:
    def __init__(self):
        self.key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

    def load_or_generate_key(self):
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
            return key

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()
