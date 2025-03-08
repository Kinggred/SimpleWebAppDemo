from sqlmodel import Session, create_engine, SQLModel
from SWADemo.config import settings

def create_db_and_tables():
    """
    DON'T DO THIS.
    No migrations for me
    """
    engine = create_engine(settings.POSTGRES_DSN)
    SQLModel.metadata.create_all(engine)

def get_session():
    engine = create_engine(settings.POSTGRES_DSN)
    with Session(engine) as session:
        yield session

