from sqlalchemy import Column, Integer, String, ForeignKey
# it is just a table design
# ForeignKey is used to create relationship between two tables

from sqlalchemy.orm import relationship
# relationship is used to define one-to-many connection between User and Note

from database import Base

# table 1 : users table
class User(Base):
# class used to define structure of users table

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # id is the primary key and auto-increments for each new user

    name = Column(String)
    # full name of the user

    email = Column(String, unique=True)
    # email must be unique , used for login

    password = Column(String)
    # password will be stored as hashed value , never plain text

    notes = relationship("Note", back_populates="owner")
    # one user can have many notes
    # back_populates connects Note.owner back to User.notes


# table 2 : notes table
class Note(Base):
# class used to define structure of notes table

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # id is the primary key and auto-increments for each new note

    title = Column(String)
    # short title of the note

    content = Column(String)
    # full content / body of the note

    owner_id = Column(Integer, ForeignKey("users.id"))
    # foreign key linking this note to the user who created it
    # ForeignKey("users.id") means owner_id must match an id in the users table

    owner = relationship("User", back_populates="notes")
    # connects Note back to the User who owns it
