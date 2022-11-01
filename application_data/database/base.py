from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite+pysqlite:///application_data/database/test.db", echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
