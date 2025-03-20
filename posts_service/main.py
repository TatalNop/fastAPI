from fastapi import FastAPI, HTTPException,status
import json
from  database.database import SessionLocal, database_create, create_table, Post,User
from config.schemas import UserWithPostsOut,PostsIn,Posts, UpdatePost
from typing import List

app = FastAPI()

database_create()
create_table()
db = SessionLocal()

#Endpoint to get all post
@app.get("/posts/all", response_model=List[Posts])
async def get_all_posts():
    try:
        posts = db.query(Post).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Posts found.")
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#Endpoint to search by user
@app.get("/posts/user", response_model=UserWithPostsOut)
async def search_user(username : str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

#Endpoint to add post
@app.post("/posts/add", response_model=PostsIn)
async def add_user(post_data : PostsIn):
    user = db.query(User).filter(User.id == post_data.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_post = Post(
        title=post_data.title,
        body=post_data.body,
        user_id=user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post_data

#Endpoint to update post
@app.put("/posts/post_id", response_model=Posts)
async def update_post(post_id: int, post: UpdatePost):
    try:
        existing_post = db.query(Post).filter(Post.id == post_id).first()
        if not existing_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if post.title:
            existing_post.title = post.title
        if post.body:
            existing_post.body = post.body

        db.commit()
        db.refresh(existing_post)
        return existing_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
#Endpoint to delete post
@app.delete("/posts/post_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
