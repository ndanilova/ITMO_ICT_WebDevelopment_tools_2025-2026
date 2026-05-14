import asyncio

import aiohttp
from bs4 import BeautifulSoup

from core.async_db import AsyncSessionLocal
from core.db.models.task import Task

_parse_semaphore = asyncio.Semaphore(5)


async def save_task(title: str, url: str) -> None:
    async with AsyncSessionLocal() as session:
        task = Task(title=title, description=url)
        session.add(task)
        await session.commit()
        await session.refresh(task)


async def parse_page(session: aiohttp.ClientSession, url: str) -> None:
    async with _parse_semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                raw_title = soup.title.string if soup.title else None
                title = raw_title.strip() if raw_title else "No title"
                await save_task(title, url)
        except Exception as exc:
            print(f"Error on {url}: {exc}")
