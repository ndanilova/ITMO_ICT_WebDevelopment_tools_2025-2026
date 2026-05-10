import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LAB1_DIR = BASE_DIR / "laboratory_work_1"

sys.path.append(str(LAB1_DIR))


from bs4 import BeautifulSoup
import requests

from sqlmodel import Session

from core.db import engine
from db.models.task import Task


def save_task(title: str, url: str):
    with Session(engine) as session:
        task = Task(
            title=title,
            description=url
        )

        session.add(task)
        session.commit()


def parse_page(url: str):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title"

    save_task(title, url)

    print(f"Saved: {title}")