# FastAPI Time Management Application

## Project Description

Server-side application for personal time management:

- Task creation with deadlines, statuses, and priorities
- Time tracking by task
- Optional notifications and daily schedule planning
- JWT-based authentication and protected API

## Tech Stack

- Python 3.10+
- FastAPI
- SQLModel + SQLAlchemy
- PostgreSQL
- Alembic migrations
- JWT (`PyJWT`)
- Password hashing (`passlib` + `bcrypt`)

## Database Models

Implemented entities:

1. `User`
2. `Task`
3. `TimeLog`
4. `Tag`
5. `TaskTag` (association with descriptive field `added_at`)
6. `Notification`
7. `ScheduleDay`
8. `ScheduleItem`

Relationships:

- One-to-many: `User -> Task`, `Task -> TimeLog`, `Task -> Notification`, `User -> ScheduleDay`, `ScheduleDay -> ScheduleItem`
- Many-to-many: `Task <-> Tag` via `TaskTag`

## Migrations

Alembic is configured in:

- `alembic.ini`
- `migrations/env.py`
- `migrations/versions/`

Apply migrations:

```bash
alembic upgrade head
```

## Database Connection

Connection is configured in `core/db.py` through environment variable:

- `DB_URL`

## Authentication

Implemented manual auth flow:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/change-password`

Protected endpoints require `Authorization: Bearer <token>`.

## API Endpoints

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/change-password`

### Users

- `POST /users/`
- `GET /users/`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`

### Tasks

- `POST /tasks/`
- `GET /tasks/`
- `GET /tasks/{task_id}` (nested response with related entities)
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

## Demonstration

The project is demonstrated through FastAPI Swagger UI at `/docs`.
