import logging
from typing import TypeVar, Generic, Type, List
from uuid import UUID

from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlmodel import Session, select, SQLModel

from SWADemo.models.base import BaseModel

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def db_add(self, db: Session, object_to_add: ModelType) -> ModelType:
        try:
            db.add(object_to_add)
            db.commit()
            db.refresh(object_to_add)
        except IntegrityError as error:
            logger.error(f"Database error: {error.orig}")
        logger.info(f"Added {self.model.__name__}: {object_to_add.id}")

        return object_to_add

    def get(self, db: Session, id: UUID) -> ModelType | None:
        data = db.exec(select(self.model).where(self.model.enabled, self.model.id == id)).first()
        if data:
            logger.info(f"Retreived {self.model.__name__}: {id}")
            return data

    def get_multi(self, db: Session, limit: int) -> List[ModelType]:
        obj = db.exec(select(self.model).where(self.model.enabled).limit(limit)).all()
        logger.info(f"Retreived {len(obj)} {self.model.__name__}s")

        return obj

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        obj = self.db_add(db=db, object_to_add=db_obj)
        logger.info(f"Created {self.model.__name__}: {obj.id}")

        return obj

    def remove(self, db: Session, *, id: UUID) -> ModelType:
        db_obj = db.exec(select(self.model).where(self.model.enabled, self.model.id == id)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not found")
        db_obj.enabled = False
        db.commit()
        logger.info(f"Removed {self.model.__name__}: {db_obj.id}")

        return db_obj
