import asyncio
import os

import aiohttp
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
)


@celery_app.task(name="run_parsing_task")
def run_parsing_task(url: str) -> dict[str, str | int]:
    from parser_service.logic import parse_page

    async def _run():
        async with aiohttp.ClientSession() as session:
            return await parse_page(session, url)

    task = asyncio.run(_run())
    return {"status": "ok", "url": url, "title": task.title, "task_id": task.id}
