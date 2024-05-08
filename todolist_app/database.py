from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

POSTGRES_DIALECT = 'postgresql'
POSTGRES_SERVER = 'localhost'
POSTGRES_DBNAME = 'todolist'
POSTGRES_SCHEMA = 'public' 
POSTGRES_USERNAME = 'postgres' 
POSTGRES_PASSWORD = 'eyeDGAF<3'


postgres_str = ('{dialect}://{username}:{password}@{server}/{dbname}'.format(
                    dialect=POSTGRES_DIALECT,
                    server=POSTGRES_SERVER,
                    dbname=POSTGRES_DBNAME,
                    username=POSTGRES_USERNAME,
                    password=POSTGRES_PASSWORD
                ))
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:eyeDGAF<3@postgresserver/db"

engine = create_engine(
    postgres_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()