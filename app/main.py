from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
import app.database as database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, hashed_password=user.password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/messages/", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(subject=message.subject, body=message.body, recipient_id=message.recipient_id, sender_id=1)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/users/{user_id}/inbox", response_model=List[schemas.Inbox])
def read_inbox(user_id: int, db: Session = Depends(get_db)):
    inbox_items = db.query(models.Inbox).filter(models.Inbox.user_id == user_id).all()
    return inbox_items
