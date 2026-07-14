import re

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.chat import ChatData, ChatReference, ChatRequest
from data.place_loader import load_place_dataset


def _terms(message: str) -> list[str]:
    return [term for term in re.findall(r"[가-힣A-Za-z0-9]+", message.lower()) if len(term) >= 2]


def create_grounded_answer(db: Session, payload: ChatRequest) -> ChatData:
    terms = _terms(payload.message)
    places = load_place_dataset()
    matched_places = [place for place in places if any(
        term in " ".join([place.get("title", ""), place.get("address", ""), " ".join(place.get("tags", []))]).lower()
        for term in terms
    )][:3]

    posts: list[Post] = []
    if terms:
        conditions = [or_(Post.title.ilike(f"%{term}%"), Post.content.ilike(f"%{term}%")) for term in terms]
        posts = list(db.scalars(select(Post).where(or_(*conditions)).order_by(Post.id.desc()).limit(3)).all())

    references = [ChatReference(type="place", id=place["contentId"], title=place["title"]) for place in matched_places]
    references += [ChatReference(type="post", id=str(post.id), title=post.title) for post in posts]
    if matched_places:
        names = ", ".join(place["title"] for place in matched_places)
        answer = f"제공된 지역 정보에서 요청과 관련된 장소로 {names}을(를) 찾았습니다. 자세한 내용은 함께 표시된 출처를 확인해 주세요."
    elif posts:
        names = ", ".join(post.title for post in posts)
        answer = f"커뮤니티에서 요청과 관련된 글로 {names}을(를) 찾았습니다. 게시글 내용을 참고해 주세요."
    else:
        answer = "제공된 장소와 게시글에서 질문을 뒷받침할 정보를 찾지 못했습니다. 지역이나 장소 유형을 포함해 다시 질문해 주세요."
    return ChatData(answer=answer, references=references)
