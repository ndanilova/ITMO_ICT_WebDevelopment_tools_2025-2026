from fastapi import Depends, FastAPI
from pydantic import BaseModel, HttpUrl

from app.api.deps import get_current_user
from app.api.routes import auth, notification, schedule, tag, task, task_tag, timelog, user
from celery_app import run_parsing_task

app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router, dependencies=[Depends(get_current_user)])
app.include_router(user.router, dependencies=[Depends(get_current_user)])
app.include_router(tag.router, dependencies=[Depends(get_current_user)])
app.include_router(task_tag.router, dependencies=[Depends(get_current_user)])
app.include_router(timelog.router, dependencies=[Depends(get_current_user)])
app.include_router(notification.router, dependencies=[Depends(get_current_user)])
app.include_router(schedule.router, dependencies=[Depends(get_current_user)])


@app.get("/")
def hello() -> str:
    return "Hello, andan!"


class AsyncParseRequest(BaseModel):
    url: HttpUrl


@app.post("/async-parse")
async def async_parse(body: AsyncParseRequest) -> dict[str, str]:
    run_parsing_task.delay(str(body.url))
    return {"message": "Task sent to queue", "url": str(body.url)}
