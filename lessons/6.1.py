from fastapi import FastAPI, Depends, Query
import subprocess
import time

app = FastAPI()

# Функция зависимости:
def user_dep(name: str = Query(...), password: str = Query(...)):
    return {"name": name, "valid": True}

# Функция пути/конечная точка веб-приложения:
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user


if __name__ == "__main__":
    import uvicorn
    import os

    # Запуск SSH-туннеля в фоновом режиме
    serveo_command = [
        "ssh",
        "-R", "80:localhost:8000",
        "serveo.net",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-n"
    ]
    process = subprocess.Popen(serveo_command)

    # Даем немного времени для установления туннеля
    time.sleep(5)

    # Запуск FastAPI сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Завершение работы SSH-туннеля при выходе
    process.terminate()
    process.wait()
