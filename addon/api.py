from fastapi import FastAPI

from addon.endpoints import (
    addon,
)

app = FastAPI()

app.include_router(addon.router)
