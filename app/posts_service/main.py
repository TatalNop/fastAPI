from fastapi import FastAPI, HTTPException,status
import json
from  database.database import Base, engine, SessionLocal
from  database.model import Post,User
from config.schemas import UserWithPostsOut,PostsIn,Posts
app = FastAPI()

#create databases and import data
Base.metadata.create_all(bind=engine)
db = SessionLocal()
if db.query(Post).count() == 0:
    with open('posts_service/posts.json') as f:
        posts_data = json.load(f)

    for post in posts_data:
        post_data = {
            "id": post["id"],
            "title": post["title"],
            "body": post["body"],
            "user_id": post["userId"]
        }
        db.add(Post(**post_data))
    db.commit()

@app.get("/posts/all", response_model=Posts)
async def get_all_posts():
    try:
        posts = db.query(Post).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Posts found.")
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get("/posts/user", response_model=UserWithPostsOut)
async def search_user(username : str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.post("/posts/add", response_model=PostsIn)
async def search_user(post_data : PostsIn):
    user = db.query(User).filter(User.username == post_data.username).first()
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