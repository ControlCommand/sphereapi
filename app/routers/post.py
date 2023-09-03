from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: dict = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    
    # this query returns all the posts made by the current logged in user.
    # if i want the user to get all posts, i would have to remove the 'models.Post.owner_id == current_user.id' bit.
    
    # posts =db.query(models.Post).filter(
        # models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id,
            isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id,
                                                          models.Post.title.contains(search)).limit(limit).offset(skip).all()    
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Posts Were Found")

    
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):

    # sql way
    '''
    # cursor.execute(
    #     """
    #     INSERT INTO Posts (title, content)
    #     VALUES (%s, %s) RETURNING *
    #     """,
    #     (post.title, post.content))
    
    # new_post = cursor.fetchone()
    # conn.commit()
'''    
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    
    # this is the other sql way
    '''
    # cursor.execute(
    #     """
    #     SELECT * FROM Posts WHERE id=%s
    #     """,
    #     (id,))
    
    # post = cursor.fetchone()
    '''
    #  post = db.query(models.Post).filter(models.Post.id == id).one_or_none()
    
    post_query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id,
            isouter=True).group_by(models.Post.id).filter(models.Post.id == id)

    post = post_query.one_or_none()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found")

        
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with ID {id} was not found")
    post, votes = post

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    gotten_post = schemas.PostOut(Post=post, votes=votes)

    return gotten_post





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    '''    
    # cursor.execute(
    #     """
    #     DELETE FROM Posts WHERE id=%s RETURNING *
    #     """,
    #     (id,)
    # )
    # deleted_post = cursor.fetchone()
    '''
    queried_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = queried_post.one_or_none()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    queried_post.delete(synchronize_session= False)
    
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    
    '''
    # cursor.execute(
    #     """
    #     UPDATE Posts SET title=%s, content=%s, published=%s
    #     WHERE id=%s
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    '''
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.one_or_none()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.one_or_none()

