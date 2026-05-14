import os
from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
)

@celery_instance.task(name="run_parsing_task")
def run_parsing_task(url: str):
    # Здесь мы вызываем парсер. 
    # Так как Celery работает синхронно, используем библиотеку requests 
    # или запускаем асинхронный цикл внутри
    import asyncio
    from parser_service.parser_logic import parse_page
    # запуск асинхронного парсера в синхронном воркере
    asyncio.run(start_parse_logic(url))