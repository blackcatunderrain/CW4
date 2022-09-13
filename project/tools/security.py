import base64
import calendar
import datetime
import hashlib
from typing import Union
import jwt
from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def generate_token(email, password, password_hash, refresh=False):
    if not email:
        return None
    if not refresh:
        if not compose_passwords(password_hash=password_hash, password=password):
            return None

    data = {
        "email": email,
        "password": password
    }

    min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
    data['exp'] = calendar.timegm(min15.timetuple())
    access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    days130 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_DAYS"])
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def update_token(refresh_token):
    data = jwt.decode(refresh_token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])

    email = data.get("email")
    password = data.get("password")

    return generate_token(email=email, password=password, password_hash=None, refresh=True)


def compose_passwords(password_hash: Union[str, bytes], password: str):
    return password_hash == generate_password_hash(password)


def get_data_by_token(refresh_token):
    data = jwt.decode(refresh_token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])
    return data


