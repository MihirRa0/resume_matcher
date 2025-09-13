from sqlalchemy.orm import Session
from app.services import auth_service 
from app.models import users
from app.schemas import user


def get_user_by_email(db:Session,email:str):
    return db.query(users.User).filter(users.User.email == email).first()

def create_user(db: Session, user: user.UserCreate):
    hashed_password=auth_service.get_password_hash(user.password)
    db_user = users.User(email = user.email,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

