from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import AdUser, Task
from app.schemas import CreateUser, UpdateUser
from slugify import slugify



router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(AdUser)).all()
    return users


@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(AdUser).filter(AdUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    existing_user = db.query(AdUser).filter_by(username=create_user.username).first()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with username {create_user.username} already exists.')

    db.execute(insert(AdUser).values(
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        age=create_user.age,
        slug=slugify(create_user.username)
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{user_id}')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.query(AdUser).filter(AdUser.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

    db.execute(update(AdUser).where(AdUser.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete/{user_id}')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(AdUser).filter(AdUser.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

    tasks = db.query(Task).filter(Task.user_id == user_id).one_or_none()
    if tasks is not None:
        db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(AdUser).where(AdUser.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}


@router.get('/{user_id}/tasks')
async def task_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(AdUser).filter(AdUser.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks if tasks else {'status_code': status.HTTP_404_NOT_FOUND, 'detail': 'No tasks found for this user'}