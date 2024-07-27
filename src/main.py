import subprocess
import uvicorn
from fastapi import FastAPI
from web import explorer, creature, user, inst

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
app.include_router(inst.router)
if __name__ == "__main__":
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
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    finally:
        # Завершение работы SSH-туннеля при выходе
        process.terminate()
        process.wait()


