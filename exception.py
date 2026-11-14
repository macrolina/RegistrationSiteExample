class CryptographyError(Exception):
    def __init__(self, message, code):
        self.message=message
        self.code=code

    def __str__(self):
        return self.message

class MasterKeyNotFoundError(CryptographyError):
    def __init__(self, message="MASTER_KEY/BLIND_KEY is not found. Create file .env or insert value.", code=404):
        self.message=message
        self.code=code

    def __str__(self):
        return self.message

class MasterKeySecurityError(CryptographyError):
    def __init__(self, message="MASTER_KEY/BLIND_KEY has less than 44/64 symbols in it. "
                               "Create it using following command:  "
                               "print(cryptography.fernet.Fernet.generate_key().decode())", code=416):
        self.message=message
        self.code=code

    def __str__(self):
        return self.message
