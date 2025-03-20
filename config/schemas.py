from pydantic import BaseModel
from typing import List, Optional
class Token(BaseModel):
    access_token: str

class TokenRequest(BaseModel):
    client_id : str
    client_secret : str

class Users(BaseModel):
    id  : int
    name : str
    username : str
    email : str

class Posts(BaseModel):
    user_id : int
    id : int
    title : str
    body : str

class PostOutUser(BaseModel):
    user_id : int
    username : str
    title : str
    body : str

class AddPosts(BaseModel):
    user_id : int
    title : str
    body : str

class PostsIn(BaseModel):
    username : str
    title : str
    body : str

class UserWithPostsOut(BaseModel):
    id: int
    name: str
    username: str
    email: str
    posts: List[Posts]

class UpdateUser(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None

class UpdatePost(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
