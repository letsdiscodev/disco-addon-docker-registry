from fastapi import APIRouter

from addon import keyvalues, storage
from addon.models.db import Session

router = APIRouter()


@router.get("/addon")
def addon_get():
    with Session.begin() as dbsession:
        return {
            "addon": {
                "version": keyvalues.get_value(dbsession, key="ADDON_VERSION"),
            },
        }
