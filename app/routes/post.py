from sqlalchemy.sql.functions import current_user, func
from app import oauth2
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional


router = APIRouter(
	prefix="/posts",
	tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostWithVote])
def get_posts(
	db: Session = Depends(get_db),
	current_user: int = Depends(oauth2.get_current_user),
	limit: int = 4,
	skip: int = 0,
	search: Optional[str] = ""
):
	# posts = db.\
	# 	query(models.Post).\
	# 	filter(models.Post.title.contains(search)).\
	# 	limit(limit).\
	# 	offset(skip).\
	# 	all()
	results = db\
		.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
		.join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
		.group_by(models.Post.id)\
		.filter(models.Post.title.contains(search))\
		.limit(limit)\
		.offset(skip)\
		.all()
	return results

@router.post('/',
	status_code=status.HTTP_201_CREATED,
	response_model=schemas.PostResponse)
def create_posts(
	post: schemas.PostCreate,
	db: Session = Depends(get_db),
	current_user: int = Depends(oauth2.get_current_user)
):
	new_post = models.Post(
		title=post.title,
		content=post.content,
		owner_id=current_user.id
	)
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post

@router.get(
	'/{id}', status_code=status.HTTP_200_OK,
	response_model=schemas.PostWithVote
)
def get_post(
	id: int,
	db: Session = Depends(get_db),
	current_user: int = Depends(oauth2.get_current_user)
):
	# post = db.\
	# 	query(models.Post).\
	# 	filter(models.Post.id == id).\
	# 	first()
	post = db\
		.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
		.join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
		.group_by(models.Post.id)\
		.filter(models.Post.id == id)\
		.first()
	if not post:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Post not founded"
		)
	return post

@router.delete(
	'/{id}',
	status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
	id: int,
	db: Session = Depends(get_db),
	current_user: int = Depends(oauth2.get_current_user)
):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	post = post_query.first()
	if post == None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"poast with id: {id} does not exist"
		)
	if post.owner_id != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Not authorized to perform requested action"
		)
	post_query.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put(
	'/{id}',
	response_model=schemas.PostResponse
)
def update_post(
	id: int,
	updated_post: schemas.PostUpdate,
	db: Session = Depends(get_db),
	current_user: int = Depends(oauth2.get_current_user)
):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	post = post_query.first()
	if post == None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Post with id: {id} does not exist."
		)
	if post.owner_id != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Not authorized to perform requested action"
		)
	post_query.update(updated_post.dict(), synchronize_session=False)
	db.commit()
	return post_query.first()

# ? SQL Section
# @app.get('/posts')-> None
# def get_posts():
# 	cursor.execute("SELECT * FROM posts")
# 	posts = cursor.fetchall()
# 	return { "data": posts }

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
# 	cursor.execute(
# 		"""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
# 		(post.title, post.content, post.published)
# 	)
# 	new_post = cursor.fetchone()
# 	connection.commit()
# 	return { "data": new_post }

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
# 	cursor.execute(
# 		"""SELECT * FROM posts where id = %s""",
# 		(str(id))
# 	)
# 	post = cursor.fetchone()
# 	if not post:
# 		raise HTTPException(
# 			status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"post with id: {id} was not found"
# 		)
# 	return { "post_detail": post }

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
# 	cursor.execute(
# 		"""DELETE FROM posts WHERE id = %s RETURNING *""",
# 		(str(id))
# 	)
# 	connection.commit()
# 	deleted_post = cursor.fetchone()
# 	if deleted_post == None:
# 		raise HTTPException(
# 			status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"Post with id: {id} does not exist"
# 		)
# 	return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put('/posts/{id}')
# def update_posts(id: int, post: Post):
# 	cursor.execute(
# 		"""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
# 		(post.title, post.content, post.published, id)
# 	)
# 	updated_post = cursor.fetchone()
# 	connection.commit()
# 	if updated_post == None:
# 		raise HTTPException(
# 			status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"Post with id: {id} does not exist"
# 		)
# 	return { "message": updated_post }