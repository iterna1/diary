from werkzeug.security import generate_password_hash, check_password_hash
import datetime


def password_exists(hash, password):
    if check_password_hash(hash, password):
        return True


def to_hash(password):
    return generate_password_hash(password)


def get_date():
    return datetime.datetime.now().__str__().split()
