from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from metadata_embedding_explorer.models import Base, Comparison, Embedding, Metadata


def store_in_database(db_connection: str, data: Union[Metadata, Embedding, Comparison]) -> None:
    session = get_session(db_connection)
    session.add_all(data)
    session.commit()


def get_session(db_connection: str) -> Session:
    engine = create_engine(db_connection)
    return sessionmaker(bind=engine)()


def initialize_database(db_connection: str) -> None:
    engine = create_engine(db_connection)
    Base.metadata.create_all(engine)
