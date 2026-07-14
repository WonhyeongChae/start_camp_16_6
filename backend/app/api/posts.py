from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import SuccessEnvelope
from app.schemas.post import PostCreate, PostDeleteRequest, PostListData, PostRead, PostUpdate
from app.services.posts import create_post, delete_post, get_post, list_posts, update_post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=SuccessEnvelope[PostListData])
def read_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    category: str | None = None,
    keyword: str | None = None,
    sort: str = "latest",
    db: Session = Depends(get_db),
):
    data = list_posts(db, page=page, size=size, category=category, keyword=keyword, sort=sort)
    return SuccessEnvelope[PostListData](data=data, message="목록을 조회했습니다.")


@router.get("/{post_id}", response_model=SuccessEnvelope[PostRead])
def read_post(post_id: int, db: Session = Depends(get_db)):
    data = get_post(db, post_id)
    return SuccessEnvelope[PostRead](data=data, message="게시글을 조회했습니다.")


@router.post("", response_model=SuccessEnvelope[PostRead], status_code=201)
def write_post(payload: PostCreate, db: Session = Depends(get_db)):
    data = create_post(db, payload)
    return SuccessEnvelope[PostRead](data=data, message="게시글을 등록했습니다.")


@router.put("/{post_id}", response_model=SuccessEnvelope[PostRead])
def edit_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    data = update_post(db, post_id, payload)
    return SuccessEnvelope[PostRead](data=data, message="게시글을 수정했습니다.")


@router.delete("/{post_id}", response_model=SuccessEnvelope[dict[str, int]])
def remove_post(post_id: int, payload: PostDeleteRequest, db: Session = Depends(get_db)):
    data = delete_post(db, post_id, payload)
    return SuccessEnvelope[dict[str, int]](data=data, message="게시글을 삭제했습니다.")