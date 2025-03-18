from fastapi import FastAPI, HTTPException,status
import json
from  database.database import Base, engine ,SessionLocal
from  database.model import User
from config.schemas import Users

app = FastAPI()

#create databases and import data
Base.metadata.create_all(bind=engine)
db = SessionLocal()
if db.query(User).count() == 0:
    with open('users_service/users.json') as f:
        users_data = json.load(f)

    for user in users_data:
        users_data = {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"]
        }
        db.add(User(**users_data))
    db.commit()


#endpoint
@app.get("/users/all",response_model=list[Users])
async def get_all_user():
    try:
        users = db.query(User).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/")
async def get_user_by_username(username : str):
   user = db.query(User).filter(User.username == username).first()
   if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   return user