from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from ..models import Vote
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_cur_user
from .. import models, schemas

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user=Depends(get_cur_user)):

    is_post_exist = db.query(models.Post).filter(
        models.Post.id == vote.post_id).first()

    if(not is_post_exist):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(Vote).filter(
        Vote.user_id == current_user.id, Vote.post_id == vote.post_id)
    vote_res = vote_query.first()

    if(vote.direction == 0):
        if(not vote_res):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "vote deleted successfully"}

    else:
        if(vote_res):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You already voted for this post")

        new_vote = Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.VoteResponse])
def get_votes(db: Session = Depends(get_db), current_user=Depends(get_cur_user)):
    votes = db.query(Vote).filter(Vote.user_id == current_user.id).all()
    return votes
