from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecate='auto')

def get_hashed_password(password):
    return pwd_context(password)
