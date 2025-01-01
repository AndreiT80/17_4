# Домашнее задание по теме "Использование БД в маршрутизации. 1.1" Modul 17-4


from fastapi import FastAPI
from app.routers import *  # Импорт маршрутов
from sqlalchemy import create_engine
from app.backend.db import Base  # Импорт Base
from app.routers.user import router as user_router  # Импортируем router

app = FastAPI()

app.include_router(user_router, prefix="/users")

@app.get("/")
async def welcome():
    return {"message": "Welcome to TaskManager"}



# Создаем движок SQLAlchemy
engine = create_engine('sqlite:///taskmanager.db', connect_args={"check_same_thread": False}, echo=True)

# Создаем таблицы в базе данных на основе метаданных моделей
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("База данных и таблицы созданы успешно.")

# pip install sqlalchemy
# pip install fastapi
# pip install uvicorn
# pip install python-slugify

# загрузка    uvicorn app.main:app
# загрузка    python -m app.main