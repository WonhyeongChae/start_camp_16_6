from math import ceil

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostDeleteRequest, PostListData, PostListItem, PostRead, PostUpdate


ALLOWED_CATEGORIES = {"여행", "맛집", "축제", "생활", "자유"}
ALLOWED_SORTS = {"latest", "views"}


def _to_post_read(post: Post) -> PostRead:
    return PostRead(
        id=post.id,
        title=post.title,
        content=post.content,
        category=post.category,
        nickname=post.nickname,
        view_count=post.view_count,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def _to_post_list_item(post: Post) -> PostListItem:
    return PostListItem(
        id=post.id,
        title=post.title,
        content=post.content,
        category=post.category,
        nickname=post.nickname,
        view_count=post.view_count,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def _validate_list_params(page: int, size: int, category: str | None, sort: str) -> None:
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="페이지 값이 올바르지 않습니다.")

    if category and category != "all" and category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=400, detail="게시글 카테고리가 올바르지 않습니다.")

    if sort not in ALLOWED_SORTS:
        raise HTTPException(status_code=400, detail="정렬 기준이 올바르지 않습니다.")


def list_posts(
    db: Session,
    page: int = 1,
    size: int = 10,
    category: str | None = None,
    keyword: str | None = None,
    sort: str = "latest",
) -> PostListData:
    _validate_list_params(page, size, category, sort)

    base_query = select(Post)

    if category and category != "all":
        base_query = base_query.where(Post.category == category)

    if keyword:
        like_keyword = f"%{keyword}%"
        base_query = base_query.where(
            (Post.title.ilike(like_keyword)) | (Post.content.ilike(like_keyword))
        )

    total = db.scalar(select(func.count()).select_from(base_query.subquery())) or 0

    if sort == "views":
        base_query = base_query.order_by(Post.view_count.desc(), Post.id.desc())
    else:
        base_query = base_query.order_by(Post.created_at.desc(), Post.id.desc())

    items = db.scalars(base_query.offset((page - 1) * size).limit(size)).all()

    return PostListData(
        items=[_to_post_list_item(post) for post in items],
        page=page,
        size=size,
        total=total,
        total_pages=ceil(total / size) if total else 0,
    )


def get_post_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


def get_post(db: Session, post_id: int) -> PostRead:
    post = get_post_or_404(db, post_id)
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return _to_post_read(post)


def create_post(db: Session, payload: PostCreate) -> PostRead:
    post = Post(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        nickname=payload.nickname,
        password=payload.password,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return _to_post_read(post)


def update_post(db: Session, post_id: int, payload: PostUpdate) -> PostRead:
    post = get_post_or_404(db, post_id)

    if post.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    post.title = payload.title
    post.content = payload.content
    post.category = payload.category
    post.nickname = payload.nickname
    db.commit()
    db.refresh(post)
    return _to_post_read(post)


def delete_post(db: Session, post_id: int, payload: PostDeleteRequest) -> dict[str, int]:
    post = get_post_or_404(db, post_id)

    if post.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return {"id": post_id}