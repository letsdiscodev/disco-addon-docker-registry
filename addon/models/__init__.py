from sqlalchemy.orm import configure_mappers

from addon.models.user import User  # noqa: F401

configure_mappers()
