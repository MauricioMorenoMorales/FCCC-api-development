from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class UserResponse(BaseModel):
	email: EmailStr
	id: int
	class Config:
		orm_mode = True

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True
	# rating: Optional[int] = None

class PostResponse(PostBase):
	created_at: datetime
	id: int
	owner_id: int
	owner: UserResponse
	class Config:
		orm_mode = True

class PostWithVote(BaseModel):
	Post: PostResponse
	votes: int

class PostCreate(PostBase):
	pass

class PostUpdate(PostBase):
	pass


class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None

class Vote(BaseModel):
	post_id: int
	dir: conint(le=1)