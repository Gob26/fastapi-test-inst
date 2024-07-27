from fastapi import FastAPI, Depends

app = FastAPI()

# Функция зависимости
def check_dep(name: str, password: str):
    if not name:
        raise ValueError("Name is required")
    # Можно добавить здесь дополнительные проверки или логику для password, если нужно
    return True

# Путь/конечная точка веб-приложения
@app.get("/check_user", dependencies=[Depends(check_dep)])
def check_user() -> bool:
    return True
