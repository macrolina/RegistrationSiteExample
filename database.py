from cryptography.fernet import Fernet
from sqlalchemy import Column, Integer, String, LargeBinary, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.hybrid import hybrid_property
from exception import MasterKeyNotFoundError, MasterKeySecurityError
from dotenv import load_dotenv
import hmac
import hashlib
import os

load_dotenv()

MASTER_KEY=os.getenv("MASTER_KEY")
BLIND_KEY=os.getenv("BLIND_KEY")
if not MASTER_KEY or not BLIND_KEY:
    raise MasterKeyNotFoundError
elif len(MASTER_KEY)<44 or len(BLIND_KEY)!=64:
    raise MasterKeySecurityError

BLIND_KEY=bytes(BLIND_KEY, "utf-8")

dek_encrypter=Fernet(MASTER_KEY)

Base=declarative_base()

# create blind index key
def create_blind_key(value: str):
    readable=value.strip().lower().encode("utf-8")
    return hmac.new(BLIND_KEY, readable, hashlib.sha256).hexdigest()

class Users(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True)
    encrypted_dek=Column(LargeBinary, nullable=False)

    _email=Column('email', LargeBinary, nullable=False)
    _username=Column('username', LargeBinary, nullable=False)
    _password=Column('password', LargeBinary, nullable=False)

    email_index=Column(String(64), unique=True, index=True, nullable=False)
    username_index=Column(String(64), unique=True, index=True, nullable=False)

    def __init__(self, email: str, username: str, password: str):

        dek=Fernet.generate_key()

        self.encrypted_dek=dek_encrypter.encrypt(dek)

        self._dek=dek

        self.email=email
        self.username=username
        self.password=password

    # encrypter out of table
    def _get_encrypter(self):
        if not hasattr(self, "_dek") or self._dek is None:
            self._dek=dek_encrypter.decrypt(self.encrypted_dek)

        return Fernet(self._dek)

    def check_password(self, password):
        real_password=self._get_encrypter().decrypt(self._password).decode("utf-8")
        if real_password==password:
            return True
        return False

    # @hybrid_property is for auto decryption
    # @(name).setter is for auto encryption
    @hybrid_property
    def email(self):
        return self._get_encrypter().decrypt(self._email).decode("utf-8")

    @email.setter
    def email(self, value: str):
        if not value:
            raise ArgumentError("Email is required!")

        self._email=self._get_encrypter().encrypt(value.encode("utf-8"))
        self.email_index=create_blind_key(value)

    @hybrid_property
    def username(self):
        return self._get_encrypter().decrypt(self._username).decode("utf-8")

    @username.setter
    def username(self, value: str):
        if not value:
            raise ArgumentError("Username is required!")

        self._username=self._get_encrypter().encrypt(value.encode("utf-8"))
        self.username_index=create_blind_key(value,)
    @hybrid_property
    def password(self):
        return self._get_encrypter().decrypt(self._password).decode("utf-8")

    @password.setter
    def password(self, value: str):
        if not value:
            raise ArgumentError("Username is required!")

        self._password = self._get_encrypter().encrypt(value.encode("utf-8"))

engine=create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)

session=Session()

