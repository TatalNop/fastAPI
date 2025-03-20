from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config.config_file import SQL_CONFIG
import json
import logging

username = SQL_CONFIG["db_user"]
password = SQL_CONFIG["db_pass"]
server = SQL_CONFIG["db_host"]
database = SQL_CONFIG["db_name"]

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)

    # One-to-many relationship with Post
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")

# Post Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship back to User
    owner = relationship("User", back_populates="posts")


SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def database_create():
    SQLALCHEMY_URL = f"mssql+pyodbc://{username}:{password}@{server}/master?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(SQLALCHEMY_URL, isolation_level="AUTOCOMMIT")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    result = db.execute(text("SELECT name FROM sys.databases"))
    db_name = [row[0] for row in result.fetchall()]
    if database not in db_name:
       with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {database}"))
            return database
    return None

def create_table():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Insert Users
        if db.query(User).count() == 0:
            try:
                with open("database/users.json") as f:
                    users_data = json.load(f)
                db.bulk_insert_mappings(User, users_data)
                db.commit()
                logging.info("Users data inserted successfully.")
                
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Error loading users.json: {e}")
                db.rollback()
        # Insert Posts
        if db.query(Post).count() == 0:
            try:
                with open("database/posts.json") as f:
                    posts_data = json.load(f)
                
                for post in posts_data:
                    post["user_id"] = post.pop("userId")
                
                db.bulk_insert_mappings(Post, posts_data)
                db.commit()
                logging.info("Posts data inserted successfully.")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Error loading posts.json: {e}")
                db.rollback()
    except Exception as e:
        db.rollback()
        logging.error(f"Error in create_table: {e}")
    finally:
        db.close()
