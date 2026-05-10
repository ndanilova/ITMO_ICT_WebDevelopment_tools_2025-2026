import asyncio
import time

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LAB1_DIR = BASE_DIR / "laboratory_work_1"

sys.path.append(str(LAB1_DIR))

import aiohttp
from bs4 import BeautifulSoup

from core.async_db import AsyncSessionLocal
from core.async_db import async_engine
from db.models.task import Task

from urls import URLS


async def save_task(title: str, url: str):
    async with AsyncSessionLocal() as session:
        task = Task(title=title, description=url)
        session.add(task)
        await session.commit()
        await session.refresh(task)

sem = asyncio.Semaphore(5)

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