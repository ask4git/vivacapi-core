import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(select(User).where(User.uid == user_id))
    return result.scalar_one_or_none()


async def get_user_by_google_sub(db: AsyncSession, google_sub: str) -> User | None:
    result = await db.execute(select(User).where(User.google_sub == google_sub))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    email: str,
    google_sub: str,
    name: str | None = None,
    picture: str | None = None,
) -> User:
    user = User(email=email, google_sub=google_sub, name=name, picture=picture)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_profile(
    db: AsyncSession,
    user: User,
    *,
    name: str | None = None,
    picture: str | None = None,
) -> User:
    if name is not None:
        user.name = name
    if picture is not None:
        user.picture = picture
    await db.commit()
    await db.refresh(user)
    return user
