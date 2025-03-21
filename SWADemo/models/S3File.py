import logging
import re
from uuid import UUID

from pydantic import model_validator
from sqlmodel import SQLModel

logger = logging.getLogger(__name__)

class S3File(SQLModel):
    key: str
    name: str | None = None
    directory: str | None = None
    uploaded_by: UUID | None = None
    extension: str | None = None
    data: bytes | None = None

    @model_validator(mode="before")
    @classmethod
    def parse_filename(cls, value: dict):
        try:
            if "key" in value:
                value["directory"] = ""
                split_path = value["key"].split("/")
                for path in split_path[:-1]:
                    value["directory"] += path + "/"

                match = re.match(r"([^_]+)_(\w+).(\w+)", split_path[-1])

                if match:
                    value["uploaded_by"] = match.group(1)
                    value["name"] = match.group(2)
                    value["extension"] = match.group(3)
                    return value
        except TypeError:
            logger.error(f"Invalid filename: {value}")
