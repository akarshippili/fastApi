from ..schemas import PostBase, PostCreate, PostResponse, PostResponseWithVotes
from .. import models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[PostResponseWithVotes])
def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_cur_user),
              limit: int = 10, skip: int = 0, search: str = ""):

    # cursor.execute(""" SELECT * FROM post """)
    # posts = cursor.fetchall()
    # print(posts)
    # print(f'skip: {skip} limit: {limit}')
    # print(f'search {search}')

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts_with_vosts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts_with_vosts = posts_with_vosts_query.all()

    return posts_with_vosts


@router.get("/{id}", response_model=PostResponseWithVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_cur_user)):

    # # id - path params or route params
    # cursor.execute(
    #     """ SELECT * FROM post WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    return post


@router.post("/", status_code=201, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_cur_user)):  # Body(...) is a decorator

    # cursor.execute(""" INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published))
    # new = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_cur_user)):

    # cursor.execute(
    #     """ DELETE FROM post WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # post_index = [index for index, post in enumerate(all_posts) if post["id"] == id]

    post = db.query(models.Post).filter(models.Post.id == id)
    if (not post.first()):
        raise HTTPException(status_code=404, detail="post not found")
    elif(post.first().owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_cur_user)):

    # cursor.execute(""" UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (updated_post.title, updated_post.content, updated_post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if(post.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
