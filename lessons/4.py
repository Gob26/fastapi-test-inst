from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/external")
async def read_external():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://httpbin.org/get')
        return response.json()

