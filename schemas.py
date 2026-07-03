from pydantic import BaseModel
# BaseModel is used to define the structure of data and validate input data

# schema for user registration
class UserCreate(BaseModel):
# class used to define structure of registration data

    name: str
    # name must be a string

    email: str
    # email must be a string

    password: str
    # password must be a string

# UserCreate is used for new user registration
# id is not included because it is auto-incremented by the database


# schema for user login
class UserLogin(BaseModel):

    email: str
    # email must be a string , used to identify the user

    password: str
    # password must be a string

# UserLogin only needs email and password
# name is not needed during login


# schema for creating a note
class NoteCreate(BaseModel):

    title: str
    # title of the note

    content: str
    # content / body of the note

# NoteCreate is used when creating a new note
# owner_id is not included here , it will be extracted from the JWT token


# schema for note response
class NoteResponse(BaseModel):

    id: int
    # id of the note

    title: str
    # title of the note

    content: str
    # content of the note

    owner_id: int
    # id of the user who created the note

    class Config:
        from_attributes = True
        # allows SQLAlchemy model to be converted to Pydantic model
        # needed to return database objects directly as JSON response
