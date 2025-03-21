from sqlmodel import Session, SQLModel, create_engine

from SWADemo.config import settings

def get_session():
    engine = create_engine(settings.POSTGRES_DSN, connect_args={"connect_timeout": 5})
    with Session(engine) as session:
        yield session


def get_conn():
    engine = create_engine(settings.POSTGRES_DSN)
    return Session(engine)
