import aiohttp
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from parser_service.logic import parse_page

app = FastAPI(title="Parser service")


class ParseRequest(BaseModel):
    url: HttpUrl


@app.post("/parse")
async def start_parsing(body: ParseRequest) -> dict[str, str]:
    url_str = str(body.url)
    async with aiohttp.ClientSession() as session:
        await parse_page(session, url_str)
    return {"status": "success", "url": url_str}
