from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMT_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/db"

engine = create_engine(
    SQLALCHEMT_DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind = engine)

Base = declarative_base()

