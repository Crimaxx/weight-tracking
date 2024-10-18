from models import *
from scheme import *
from sqlalchemy.orm import Session
from exceptions import *
from settings  import DATABASE_URL
import bcrypt

def create_user_in_db(data:Usercreateshcema,db:Session):
    hashed_password=bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user=User(username=data.username,password=hashed_password.decode("utf-8"),height=data.height)
    user=db.query(User).filter_by(username=new_user.username).first()
    if user:
        raise UserIsExists()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"new user is created"}

def new_weight(*,data:Weightentryschema,db:Session):
    user=db.query(User).filter_by(username=data.username).first()
    user_weight=db.query(WeightEntry).filter_by(username=data.username,date=data.date).first()
    new_weight_of_user=WeightEntry(username=data.username,weight=data.weight,date=data.date)
    if not user:
        raise UserNottFoundException()
    if user_weight:
        db.query(WeightEntry).filter_by(username=data.username,date=data.date).update({"weight":data.weight})
        db.commit()
        return {"msg":"weight is added"}

    db.add(new_weight_of_user)
    db.commit()
    db.refresh(new_weight_of_user)
    return {"msg":"weight is added"}

def get_latest_weight(db: Session, username: str):
    return db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date.desc()).first()

def get_weight_change(db: Session, username: str):
    first_weight=db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date.asc()).first()
    latest_weight=db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date.desc()).first()
    return first_weight, latest_weight

def calculate_bmi(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    latest_weight = get_latest_weight(db, username)
    if user and latest_weight:
        height_in_meters = user.height / 100  
        bmi = latest_weight.weight / (height_in_meters ** 2)
        return bmi
    return None


