from datetime import timedelta, datetime
import os
from jose import jwt  # Библиотека для работы с JWT (JSON Web Tokens)
from model.user import User  # Импорт модели пользователя

# Определяем, какой модуль данных использовать, исходя из среды (тестовая или реальная база данных)
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data  # Используем тестовые данные
else:
    from data import user as data  # Используем реальные данные из базы данных

# --- Настройка аутентификации
from passlib.context import CryptContext  # Библиотека для хеширования паролей

# Секретный ключ для JWT (должен быть защищённым и не должен быть жёстко закодирован в реальном коде)
SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256"  # Алгоритм для создания и проверки JWT

# Создание контекста для хеширования паролей с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hash: str) -> bool:
    """Хеширование строки `plain` и сравнение с хешем `hash` из базы данных"""
    return pwd_context.verify(plain, hash)  # Проверка, соответствует ли пароль хешу

def get_hash(plain: str) -> str:
    """Возврат хеша строки `plain`"""
    return pwd_context.hash(plain)  # Хеширование пароля

def get_jwt_username(token: str) -> str | None:
    """Возврат имени пользователя из JWT-токена `token`"""
    try:
        # Декодирование токена и извлечение полезной нагрузки (payload)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Получение имени пользователя из полезной нагрузки токена
        username = payload.get("sub")
        if not username:  # Если имя пользователя отсутствует, возвращаем None
            return None
    except jwt.JWTError:
        return None  # Если произошла ошибка при декодировании токена, возвращаем None
    return username  # Возвращаем имя пользователя

def get_current_user(token: str) -> User | None:
    """Декодирование токена доступа OAuth и возврат объекта User"""
    # Извлекаем имя пользователя из токена
    if not (username := get_jwt_username(token)):
        return None  # Если имя пользователя не найдено, возвращаем None
    # Ищем пользователя в базе данных по имени
    if (user := lookup_user(username)):
        return user  # Возвращаем пользователя, если он найден
    return None  # Если пользователь не найден, возвращаем None

def lookup_user(username: str) -> User | None:
    """Возврат совпадающего пользователя из базы данных для строки `username`"""
    # Ищем пользователя в данных (базе или фейковых
    if (user := data.get(username)):
        return user
    return None
def auth_user(name: str, plain: str) -> User|None:
#"""Аутентификация пользователя <name> и cplain> пароль"""
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user

def create_access_token(data: dict, expires: timedelta | None = None
):
#Возвращение токена доступа с использованием JWT
    src = data.copy()
    now = datetime.utcnow()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.eпcode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#СRUD-пассивный материал
def get_all() -> list[User]:
    return data.get_all()
def get_one(name) -> User:
    return data.get_one(name)
def create(user: User) -> User:
    return data.create(user)
def modify(name: str, user: User) -> User:
    return data.modify(name, user)
def delete(name: str) -> None:
    return data.delete(name)
