from fastapi import FastAPI, Depends, HTTPException, Header

from sqlalchemy.orm import Session

from database import engine, get_db

from models import Base, User, Note

from schemas import UserCreate, UserLogin, NoteCreate, NoteResponse

from auth import hash_password, verify_password, create_access_token, verify_token
# import all functions from auth.py

app = FastAPI()

Base.metadata.create_all(bind=engine)
# this line auto creates both tables (users and notes) in the database when server starts


# Phase 6 : Register API

# registration API
@app.post("/register")

# function to register a new user
def register(user: UserCreate, db: Session = Depends(get_db)):
    # to check existing user by email
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        # use exception handling
        raise HTTPException(status_code=400, detail="Email already registered")

    # if user does not exist , create user object and hash the password
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
        # hash password before storing , never store plain text
    )

    # save user to users table
    db.add(new_user)

    db.commit()

    return {"message": "User Registered Successfully"}


# Phase 6 : Login API

# login API with JWT token generation
@app.post("/login")

# function to authenticate a user during login
def login(user: UserLogin, db: Session = Depends(get_db)):
    # find user by email in users table
    existing_user = db.query(User).filter(User.email == user.email).first()

    # verify user exists
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # verify password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect Password")

    # generate JWT token with email and name in payload
    token = create_access_token({"email": existing_user.email, "name": existing_user.name, "id": existing_user.id})
    # store email , name and id inside the token so we can use them in protected routes

    return {"access_token": token}
# return the generated token to the user after successful login


##############################################################
# helper function to get current user from JWT token
##############################################################

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    # function to extract current logged in user from JWT token

    # check if token is provided
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")

    # remove Bearer prefix from token
    token = authorization.replace("Bearer ", "")

    # verify and decode the token
    payload = verify_token(token)
    # raises exception automatically if token is invalid

    # extract email from token payload
    email = payload.get("email")

    # fetch user from database using email
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
# returns the current logged in user object


##############################################################
# Phase 6 : Create Note API
##############################################################

# create note API - protected route
@app.post("/notes")

# function to create a new note for the logged in user
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # current_user is automatically extracted from JWT token using get_current_user

    # create new note object
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
        # attach the note to the logged in user using their id
    )

    # save note to notes table
    db.add(new_note)

    db.commit()

    return {"message": "Note Created Successfully"}


##############################################################
# Phase 6 : Get Notes API
##############################################################

# get all notes for current user
@app.get("/notes")

# function to fetch all notes of the logged in user
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # fetch only notes that belong to the current logged in user

    notes = db.query(Note).filter(Note.owner_id == current_user.id).all()
    # filter by owner_id so users can only see their own notes

    return notes
# returns all notes of the current user as JSON response


##############################################################
# Phase 6 : Update Note API
##############################################################

# update note API - protected route
@app.put("/notes/{id}")

# function to update an existing note
def update_note(id: int, note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # id : note id to be updated

    # find the note by id
    existing_note = db.query(Note).filter(Note.id == id).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    # check if the current user owns this note
    if existing_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access Denied : You can only update your own notes")
    # only the note owner can update it

    # update note fields
    existing_note.title = note.title
    existing_note.content = note.content

    db.commit()

    return {"message": "Note Updated Successfully"}


##############################################################
# Phase 6 : Delete Note API
##############################################################

# delete note API - protected route
@app.delete("/notes/{id}")

# function to delete an existing note
def delete_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # id : note id to be deleted

    # find the note by id
    existing_note = db.query(Note).filter(Note.id == id).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    # check if the current user owns this note
    if existing_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access Denied : You can only delete your own notes")
    # only the note owner can delete it

    db.delete(existing_note)

    db.commit()

    return {"message": "Note Deleted Successfully"}
