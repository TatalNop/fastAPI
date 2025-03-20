from fastapi import FastAPI, HTTPException,status
import json
from  database.database import SessionLocal, User, database_create, create_table
from config.schemas import Users, UpdateUser
from typing import List

app = FastAPI()

#create databases and import data
db = SessionLocal()
database_create()
create_table()

#Endpoint to get all user
@app.get("/users/all",response_model=List[Users])
async def get_all_user():
    try:
        users = db.query(User).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#Endpoint to get user by username
@app.get("/users")
async def get_user_by_username(username : str):
   user = db.query(User).filter(User.username == username).first()
   if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   return user

#Endpoint to update user
@app.put("/users/user_id", response_model=Users)
async def update_user(user_id: int, user: UpdateUser):
    try:
        existing_user = db.query(User).filter(User.id == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Update user fields if provided
        if user.name:
            existing_user.name = user.name
        if user.username:
            existing_user.username = user.username
        if user.email:
            existing_user.email = user.email
        
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#Endpoint to delete user
@app.delete("/users/user_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
