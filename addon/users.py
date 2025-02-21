import os
import secrets
import string

from passlib.apache import HtpasswdFile
from sqlalchemy.orm.session import Session as DBSession

from addon.models import User


def generate_str() -> str:
    alphabet = string.ascii_letters + string.digits
    first_char = secrets.choice(string.ascii_letters)
    rest = "".join(secrets.choice(alphabet) for _ in range(15))
    return first_char + rest


def add_user(dbsession: DBSession) -> tuple[str, str]:
    username = generate_str()
    password = generate_str()
    add_user_to_htpasswd(username=username, password=password)
    add_user_to_db(dbsession=dbsession, username=username, password=password)
    return username, password


def add_user_to_htpasswd(username: str, password: str) -> None:
    is_new = not os.path.exists("/auth/htpasswd")
    ht = HtpasswdFile("/auth/htpasswd", new=is_new, default_scheme="bcrypt")
    ht.set_password(username, password)
    ht.save()


def add_user_to_db(dbsession: DBSession, username: str, password: str) -> None:
    user = User(
        username=username,
        password=password,
    )
    dbsession.add(user)
