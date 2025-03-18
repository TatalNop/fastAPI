from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config_file import SQL_CONFIG
import json

username = SQL_CONFIG["db_user"]
password = SQL_CONFIG["db_pass"]
server = SQL_CONFIG["db_host"]
database = SQL_CONFIG["db_name"]

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()