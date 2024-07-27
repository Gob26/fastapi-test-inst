import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from model.user import User

# Выбор сервиса данных в зависимости от среды выполнения
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service  # Использование фейкового сервиса данных для тестирования
else:
    from service import user as service  # Использование реального сервиса данных

from errors import Missing, Duplicate

# Время жизни токена доступа в минутах
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создание роутера с префиксом "/user"
router = APIRouter(prefix="/user")

# Определение зависимостей для аутентификации через OAuth2
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def unauthed():
    """Функция для вызова исключения при неудачной аутентификации"""
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Эндпоинт для получения токена доступа.
    Получает имя пользователя и пароль из формы OAuth2 и возвращает токен доступа.
    """
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Эндпоинт для получения текущего токена доступа"""
    return {"token": token}

# --- CRUD операции ---

@router.get("/")
def get_all() -> list[User]:
    """Эндпоинт для получения всех пользователей"""
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> User:
    """Эндпоинт для получения одного пользователя по имени"""
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201)
def create(user: User) -> User:
    """Эндпоинт для создания нового пользователя"""
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/{name}")
def modify(name: str, user: User) -> User:
    """Эндпоинт для обновления данных существующего пользователя"""
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}")
def delete(name: str) -> None:
    """Эндпоинт для удаления пользователя по имени"""
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
