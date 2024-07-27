import subprocess
from datetime import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

app = FastAPI()

async def doh_generator() -> AsyncGenerator[str, None]:
    yield "hello\n"
    yield "world\n"
    yield "!!!\n"

@app.get("/doh")
async def doh():
    return StreamingResponse(doh_generator(), media_type="text/plain")

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


    # Запуск FastAPI сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Завершение работы SSH-туннеля при выходе
    process.terminate()
    process.wait()