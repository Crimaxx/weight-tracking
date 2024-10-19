from fastapi import FastAPI,Depends
from db import get_db
from sqlalchemy.orm import Session
from scheme import *
from service import *
app = FastAPI()


@app.get("/")
def healthy_check():
    return {"msg":"this is my site"}

@app.post("/create_user")
def create_user(item: Usercreateshcema,db:Session=Depends(get_db)):
    message=create_user_in_db(data=item,db=db)
    return message

@app.post("/create_weight")
def create_weight(item:Weightentryschema ,db:Session=Depends(get_db)):
    message=new_weight(data=item,db=db)
    return message

@app.get("/current_weight")
def current_weight(username: str, db: Session = Depends(get_db)):
    weight = get_latest_weight(db, username)
    if weight:
        return weight
    raise HTTPException(status_code=404, detail="Weight not found.")

@app.get("/weight_change")
def weight_change(username: str, db: Session = Depends(get_db)):
    weight_change = get_weight_change(db, username)
    if weight_change:
        return  weight_change
    raise HTTPException(status_code=404, detail="No weight data found.")

@app.get("/bmi")
def get_bmi(username: str, db: Session = Depends(get_db)):
    bmi = calculate_bmi(db, username)
    if bmi:
        return {"bmi": bmi}
    raise HTTPException(status_code=404, detail="BMI could not be calculated.")