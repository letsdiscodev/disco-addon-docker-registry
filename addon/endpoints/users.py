from fastapi import APIRouter

from addon.models.db import Session
from addon.users import add_user

router = APIRouter()


@router.post("/users")
def users_post():
    with Session.begin() as dbsession:
        username, password = add_user(dbsession)
        return {
            "user": {
                "username": username,
                "password": password,
            },
        }
