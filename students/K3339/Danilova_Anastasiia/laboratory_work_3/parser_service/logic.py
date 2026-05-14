import aiohttp
from bs4 import BeautifulSoup
# Импортируем из core, так как core будет в PYTHONPATH контейнера
from core.async_db import AsyncSessionLocal
from core.db.models.task import Task

sem = asyncio.Semaphore(5)


async def save_task(title: str, url: str):
    async with AsyncSessionLocal() as session:
        task = Task(title=title, description=url)
        session.add(task)
        await session.commit()
        await session.refresh(task)



async def parse_page(session, url):
    async with sem:
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text()

                soup = BeautifulSoup(html, "html.parser")
                title = soup.title.string if soup.title else "No title"

                await save_task(title, url)

                print(f"Saved: {title}")

        except Exception as e:
            print(f"Error on {url}: {e}")


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [parse_page(session, url) for url in URLS]
        await asyncio.gather(*tasks)


start = time.time()
asyncio.run(main())
end = time.time()

print(f"Async time: {end - start}")