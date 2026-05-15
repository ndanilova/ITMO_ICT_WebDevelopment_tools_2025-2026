import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from parser_service.logic import parse_page

app = FastAPI(title="Parser service")


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResponse(BaseModel):
    status: str
    url: str
    title: str
    task_id: int


@app.post("/parse", response_model=ParseResponse)
async def start_parsing(body: ParseRequest) -> ParseResponse:
    url_str = str(body.url)
    try:
        async with aiohttp.ClientSession() as session:
            task = await parse_page(session, url_str)
    except aiohttp.ClientError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch URL: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Parse failed: {exc}") from exc

    return ParseResponse(
        status="success",
        url=url_str,
        title=task.title,
        task_id=task.id,
    )
