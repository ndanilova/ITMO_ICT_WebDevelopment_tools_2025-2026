from fastapi import FastAPI, BackgroundTasks
from pydantic import HttpUrl
import asyncio
# Импортируй логику из своего парсера
from parser_logic import parse_page 

app = FastAPI()

@app.post("/parse")
async def start_parsing(url: str):
    # Логика вызова твоего асинхронного парсера
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await parse_page(session, url)
    return {"status": "success", "url": url}