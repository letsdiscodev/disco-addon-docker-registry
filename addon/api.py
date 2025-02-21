from fastapi import FastAPI

from addon.endpoints import (
    addon,
    users,
)

app = FastAPI()

app.include_router(addon.router)
app.include_router(users.router)
