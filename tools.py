from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import session


def password_exists(hsh, password):
    if check_password_hash(hsh, password):
        return True


def to_hash(password):
    return generate_password_hash(password)


def get_date():
    return datetime.datetime.now().date()
