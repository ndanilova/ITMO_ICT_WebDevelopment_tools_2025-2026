# API

## Пример реализации

Для проверки работы были прописаны основные круды для сущености Task:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from sqlmodel import select
from db.models.task import Task, TaskCreate, TaskUpdate, TaskPublic, TaskFull

from api.deps import get_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskPublic)
def create_task(task: TaskCreate, session: Session = Depends(get_session)) -> TaskPublic:
    db_task = Task.model_validate(task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskPublic])
def get_tasks(session: Session = Depends(get_session)) -> List[TaskPublic]:
    tasks = session.exec(select(Task)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskFull)
def get_task(task_id: int, session: Session = Depends(get_session)) -> TaskFull:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
) -> TaskPublic:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted"}
```

После чего сервер был запущен по ручке документации в swagger, то есть по пути ```http://localhost:8000/docs#/```

**Результат:**

![alt text](image-1.png)

## Итоговые эндпоинты

Далее были прописаны и остальные эндпоинты, которые перечислены ниже:

### Auth

Были реализованы эндпоинты для аутентификации по путям:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/change-password`

Эндпоинты защищены с помощью требования `Authorization: Bearer <token>`.

#### **Примеры**

**Регистрация**

![alt text](image-3.png)

**Результат**

![alt text](image-2.png)

**Логин**
![alt text](image-4.png)

**Результат**

![alt text](image-5.png)

Получен токен, по которому можно далее проходить аутентификацию.

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc3NTgyNjExMH0.5lYDjRxXS5riCSr7jHo2Ky55REIjM-lIVOzn9g8sFys

Проверка:

![alt text](image-6.png)



### Users

- `POST /users/`
- `GET /users/`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`

### Tasks

- `POST /tasks/`
- `GET /tasks/`
- `GET /tasks/{task_id}` (Вложенный запрос с относящимися сущностями)
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

### Tags

- `POST /tags/`
- `GET /tags/`
- `GET /tags/{tag_id}`
- `PATCH /tags/{tag_id}`
- `DELETE /tags/{tag_id}`

### Task-Tag Association

- `POST /task-tags/`
- `GET /task-tags/`
- `GET /task-tags/{task_id}/{tag_id}`
- `PATCH /task-tags/{task_id}/{tag_id}`
- `DELETE /task-tags/{task_id}/{tag_id}`

### Time Logs

- `POST /time-logs/`
- `GET /time-logs/`
- `GET /time-logs/{time_log_id}`
- `PATCH /time-logs/{time_log_id}`
- `DELETE /time-logs/{time_log_id}`

### Notifications

- `POST /notifications/`
- `GET /notifications/`
- `GET /notifications/{notification_id}`
- `PATCH /notifications/{notification_id}`
- `DELETE /notifications/{notification_id}`

### Schedule

- Days:
  - `POST /schedule/days`
  - `GET /schedule/days`
  - `GET /schedule/days/{schedule_day_id}`
  - `PATCH /schedule/days/{schedule_day_id}`
  - `DELETE /schedule/days/{schedule_day_id}`
- Items:
  - `POST /schedule/items`
  - `GET /schedule/items`
  - `GET /schedule/items/{schedule_item_id}`
  - `PATCH /schedule/items/{schedule_item_id}`
  - `DELETE /schedule/items/{schedule_item_id}`

## Проверка работы

При попытке создать к примеру тэг, не передав токен, сервер возвращает ошибку:

![alt text](image-7.png)

При передаче токена все работает:

![alt text](image-8.png)

### POST-запросы

 **Создание задачи**

![alt text](image-9.png)

 **Создание тэга**

![alt text](image-10.png)

 **Создание уведомления**

![alt text](image-11.png)

 **Создание дня расписания**

![alt text](image-12.png)

 **Создание айтема расписания**

![alt text](image-13.png)

 **Создание временного отрезка**

![alt text](image-14.png)

### GET-запросы

**Users**

![alt text](image-15.png)

**Tasks**

![alt text](image-16.png)

**Tasks/{task_id}**

![alt text](image-17.png)

**Tags**

![alt text](image-18.png)

**Task-Tags**

![alt text](image-19.png)

**Time-Logs**

![alt text](image-20.png)

**Notifications**

![alt text](image-21.png)

**Schedule days**

![alt text](image-22.png)

**Schedule items**

![alt text](image-23.png)