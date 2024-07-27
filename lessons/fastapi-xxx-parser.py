import subprocess

from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
from bs4 import BeautifulSoup
import asyncio
from city_xxx import city_mapping

app = FastAPI()

@app.get("/m/{num}/{num2}/{city}")
async def hi(num: int, num2: int, city: str):
    # Преобразование города
    site = city_mapping.get(city.lower())
    if not site:
        raise HTTPException(status_code=400, detail="Invalid city name")

    results = []

    async def fetch_page(session, url):
        try:
            response = await session.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve {url}: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

    async with httpx.AsyncClient() as client:
        for n in range(num, num2 + 1):
            link = f'https://massage-xxx.ru/{site}/master/page/{n}'
            page_content = await fetch_page(client, link)
            soup = BeautifulSoup(page_content, 'lxml')
            block = soup.find_all("div", class_="col-md-6")
            blog_urls = [u.find("a").get("href") for u in block if u.find("a")]

            tasks = [fetch_page(client, url) for url in blog_urls]
            blog_contents = await asyncio.gather(*tasks)

            for blog_content in blog_contents:
                soup = BeautifulSoup(blog_content, 'lxml')
                cart = soup.find("div", class_="individual__info")
                phone = soup.find("a", class_="individual__call js-with-click-watch")
                description = soup.find("div", class_="individual__description-text")
                image = soup.find("img", class_="master-block__img lazy-loading ggg300")

                if cart and phone and description and image:
                    block_text = {
                        "info": cart.get_text(strip=True),
                        "phone": phone.get_text(strip=True),
                        "description": description.get_text(strip=True),
                        "image_url": image["src"]
                    }
                    results.append(block_text)
                else:
                    results.append({"error": "Элемент не найден."})
    return {"results": results}

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

    # Запуск FastAPI сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Завершение работы SSH-туннеля при выходе
    process.terminate()
    process.wait()