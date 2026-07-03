from sqlalchemy import create_engine
# create_engine is responsible to create connection between python and database

from sqlalchemy.ext.declarative import declarative_base
# declarative_base helps create database tables using Python classes instead of writing SQL manually

from sqlalchemy.orm import sessionmaker
# sessionmaker is used to create sessions that helps us to talk to the database and perform CRUD operations

import os
# os is used to read environment variables from .env file

from dotenv import load_dotenv
# load_dotenv loads the .env file so we can read DATABASE_URL from it

load_dotenv()
# load all environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
# read DATABASE_URL from .env file
# this is the Neon PostgreSQL connection string
# we never hardcode the database URL directly in the code for security reasons

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# dependency injection
def get_db():

    db = SessionLocal()
    # creates database session

    try:

        yield db
        # temporarily gives session to API

    finally:
        db.close()
        # closes session after API completes
