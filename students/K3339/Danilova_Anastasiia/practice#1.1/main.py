from fastapi import FastAPI
from typing import List
from models import Warrior, RaceType, Profession, Skill
from typing_extensions import TypedDict

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, andan!"


professions = [
     {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам"
    },
    {
        "id": 2,
        "title": "Дельфист-гребец",
        "description": "Уважаемый сотрудник"
    }
]

skills = [
    {
        "id": 1,
        "name": "Купле-продажа компрессоров",
        "description": ""
    },
    {
        "id": 2,
        "name": "Оценка имущества",
        "description": ""
    }
]

warriors = [
{
    "id": 1,
    "race": "director",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "profession": professions[0],
    "skills": skills
},
{
    "id": 2,
    "race": "worker",
    "name": "Андрей Косякин",
    "level": 12,
    "profession": professions[1],
    "skills": []
},
]

@app.get("/professions-list")
def professions_list() -> List[Profession]:
    return professions

@app.get("/profession/{profession_id}")
def professions_get(profession_id: int) -> List[Profession]:
    return [profession for profession in professions if profession.get("id") == profession_id]

@app.post("/profession")
def professions_create(profession: Profession) -> TypedDict('Response', {"status": int, "data": Profession}):
    profession_to_append = profession.model_dump()
    professions.append(profession_to_append)
    return{"status" : 200, "data": profession}

@app.delete("/profession/delete{profession_id}")
def profession_delete(profession_id: int):
    for i, profession in enumerate(professions):
        if profession.get("id") == profession_id:
            professions.pop(i)
            break
    return{"status" : 201, "message": "deleted"}

@app.put("/profession{profession_id}")
def profession_update(profession_id: int, profession: Profession) -> List[Profession]:
    for i, prof in enumerate(professions):
        if prof.get("id") == profession_id:
            profession_new = profession.model_dump
            professions[i] = profession_new
            return professions
        return professions


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return warriors

@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in warriors if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    warriors.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(warriors):
        if warrior.get("id") == warrior_id:
            warriors.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for i, war in enumerate(warriors):
        if war.get("id") == warrior_id:
            warrior_new = warrior.model_dump()
            warriors[i] = warrior_new
            return warriors
    return warriors