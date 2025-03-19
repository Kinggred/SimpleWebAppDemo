from sqlmodel import Session, SQLModel, create_engine

from SWADemo.config import settings


def create_db_and_tables():
    """
    DON'T DO THIS.
    No migrations for me
    """
    engine = create_engine(settings.POSTGRES_DSN)
    SQLModel.metadata.create_all(engine)


def get_session():
    engine = create_engine(settings.POSTGRES_DSN, connect_args={"connect_timeout": 5})
    with Session(engine) as session:
        yield session


def get_conn():
    engine = create_engine(settings.POSTGRES_DSN)
    return Session(engine)
