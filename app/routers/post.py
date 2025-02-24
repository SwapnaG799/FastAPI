
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['posts']
)
# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
    
#     posts = db.query(models.Post).all()
#     return{ "data": posts}

@router.get('/', response_model=List[schemas.Post])

async def get_post(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 10,skip: int = 0, search: Optional[str] = ""):
    # posts = cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    #print(current_user.id)
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # print(posts)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return posts
   
 


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict=post.dict()
    # post_dict['id'] = randrange(0,10000000)
   
    # my_posts.append(post_dict)
    
    # cursor.execute("""INSERT INTO posts (title,content, published)  VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    #print(current_user.id)
    #print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, title=post.title, content=post.content, published=post.published)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@router.get("/{id}",response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    #find the index in the array that has required ID
    # my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return  Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update({'title':post.title,'content':post.content}, synchronize_session=False)
    db.commit()
    
    return post_query.first()