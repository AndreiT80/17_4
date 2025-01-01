from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Создание движка для подключения к базе данных SQLite
# Здесь мы создаем базу данных с именем 'taskmanager.db' в файловой системе.
engine = create_engine('sqlite:///taskmanager.db', connect_args={"check_same_thread": False})  # Добавляем connect_args для совместимости с многопоточностью (если нужно)

# Создаем класс с декларативной основой для моделей
Base = declarative_base()  # Это основа, от которой будут наследоваться все модели

# Определяем модель User, представляющую таблицу 'users'
class User(Base):
    __tablename__ = 'users'  # Название таблицы в базе данных
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = Column(String, unique=True, nullable=False)  # Уникальное имя пользователя (обязательно для заполнения)
    firstname = Column(String, nullable=False)  # Имя пользователя (обязательно для заполнения)
    lastname = Column(String, nullable=False)  # Фамилия пользователя (обязательно для заполнения)
    age = Column(Integer, nullable=True)  # Возраст пользователя (может быть пустым)
    slug = Column(String, nullable=True)  # Слаг для пользователя, часто используется для формирования URL (может быть пустым)

# Создание локальной сессии
# Это позволяет нам взаимодействовать с базой данных, управляя транзакциями
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Настроенная сессия, связанная с нашим движком

# Если нужно, создадим все таблицы в базе данных на основе определенных моделей
Base.metadata.create_all(bind=engine)  # Создаем таблицы, если они еще не существуют