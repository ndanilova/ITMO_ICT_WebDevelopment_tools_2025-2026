from fastapi import Depends, FastAPI

from api.deps import get_current_user
from api.routes import auth, notification, schedule, tag, task, task_tag, timelog, user

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