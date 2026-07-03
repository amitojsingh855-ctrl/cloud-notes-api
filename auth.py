from passlib.context import CryptContext
# passlib is used for password hashing using bcrypt

from jose import jwt
# jose is used to create and verify JWT tokens

from fastapi import HTTPException
# HTTPException is used to raise errors when token is invalid

import os
# os is used to read environment variables

from dotenv import load_dotenv
# load_dotenv loads the .env file

load_dotenv()
# load all environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
# read SECRET_KEY from .env file
# we never hardcode the secret key directly in the code for security reasons

ALGORITHM = "HS256"
# a method used to encrypt / sign the token

# here, we are using bcrypt hashing algorithm
pwd_context = CryptContext(

    schemes=["bcrypt"],
    # use bcrypt algorithm for hashing passwords

    deprecated="auto"
    # automatically mark older hashing methods as outdated
)


# create function to hash password
def hash_password(password):

    return pwd_context.hash(password)
# use pwd_context to hash the password before storing in database


# verify password function
def verify_password(plain_password, hashed_password):

    # user enters plain password eg. pass123
    # database has hashed version eg. $2b$12$...
    # we cannot compare them directly

    return pwd_context.verify(plain_password, hashed_password)
    # return True if match , False if not


# create JWT token function
def create_access_token(data: dict):
    # data: dict means input should be in dictionary format

    token = jwt.encode(
    # encode the data into a JWT token

        data,
        # payload data to be stored inside the token eg. email, name

        SECRET_KEY,
        # secret key used to sign the token

        algorithm=ALGORITHM
        # algorithm used for signing : HS256
    )

    return token
# return the generated JWT token to the user after login


# verify JWT token function
def verify_token(token: str):
    # decode and verify the token using secret key and algorithm

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # decode the token and extract payload data

        return payload
        # return decoded payload eg. email, name

    except:

        raise HTTPException(status_code=401, detail="Invalid or Expired Token")
# raise exception if token is invalid or expired
