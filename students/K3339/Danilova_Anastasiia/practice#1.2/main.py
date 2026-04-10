from fastapi import Depends, FastAPI, HTTPException
from typing import List
from models import SkillDefault, SkillWarriorLink, Warrior, RaceType, Profession, Skill, WarriorDefault, ProfessionDefault, WarriorFull
from typing_extensions import TypedDict
from connection import init_db, get_session
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, andan!"

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()

@app.get("/skill/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    skill = session.get(Skill, skill_id)
    if not skill:   
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.post("/skill")
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Skill}):
    db_skill = Skill.model_validate(skill)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return {"status": 200, "data": db_skill}

@app.delete("/skill/delete{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(db_skill)
    session.commit()
    return {"ok": True}

@app.put("/skill{skill_id}")
def skill_update(skill_id: int, skill: SkillDefault, session=Depends(get_session))-> SkillDefault:
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_data = skill.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(db_skill, key, value)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

@app.get("/skill_warrior_links_list")
def skill_warrior_links_list(session=Depends(get_session))-> List[SkillWarriorLink]:
    return session.exec(select(SkillWarriorLink)).all()

@app.get("/skill_warrior_link/{skill_id}/{warrior_id}")
def skill_warrior_link_get(skill_id: int, warrior_id: int, session=Depends(get_session))-> SkillWarriorLink:
    skill_warrior_link = session.get(SkillWarriorLink, (skill_id, warrior_id))
    if not skill_warrior_link:
        raise HTTPException(status_code=404, detail="SkillWarriorLink not found")
    return skill_warrior_link

@app.post("/skill_warrior_link")
def skill_warrior_link_create(skill_id: int, warrior_id: int, session=Depends(get_session))-> SkillWarriorLink:
    skill_warrior_link = SkillWarriorLink(skill_id=skill_id, warrior_id=warrior_id)
    session.add(skill_warrior_link) 
    session.commit()
    session.refresh(skill_warrior_link)
    return {"status": 200, "data": skill_warrior_link}

@app.delete("/skill_warrior_link/delete{skill_id}/{warrior_id}")
def skill_warrior_link_delete(skill_id: int, warrior_id: int, session=Depends(get_session)):  
    skill_warrior_link = session.get(SkillWarriorLink, (skill_id, warrior_id))
    if not skill_warrior_link:
        raise HTTPException(status_code=404, detail="SkillWarriorLink not found")
    session.delete(skill_warrior_link)
    session.commit()
    return {"ok": True}

@app.put("/skill_warrior_link{skill_id}/{warrior_id}")
def skill_warrior_link_update(skill_id: int, warrior_id: int, new_skill_id: int, new_warrior_id: int, session=Depends(get_session)) -> SkillWarriorLink:
    skill_warrior_link = session.get(SkillWarriorLink, (skill_id, warrior_id))
    if not skill_warrior_link:
        raise HTTPException(status_code=404, detail="SkillWarriorLink not found")       
    skill_warrior_link.skill_id = new_skill_id
    skill_warrior_link.warrior_id = new_warrior_id
    session.add(skill_warrior_link)
    session.commit()
    session.refresh(skill_warrior_link)
    return skill_warrior_link

@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    profession = session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}

@app.delete("/profession/delete{profession_id}")
def profession_delete(profession_id: int, session=Depends(get_session)):
    profession = session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="Profession not found")
    session.delete(profession)
    session.commit()
    return {"ok": True}

@app.put("/profession{profession_id}")
def profession_update(profession_id: int, profession: ProfessionDefault, session=Depends(get_session)) -> ProfessionDefault:
    db_profession = session.get(Profession, profession_id)
    if not db_profession:
        raise HTTPException(status_code=404, detail="Profession not found")
    profession_data = profession.model_dump(exclude_unset=True)
    for key, value in profession_data.items():
        setattr(db_profession, key, value)
    session.add(db_profession)
    session.commit()
    session.refresh(db_profession)
    return db_profession    


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=WarriorFull)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    if not Warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}

@app.patch("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> WarriorDefault:
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    warrior_data = warrior.model_dump(exclude_unset=True)
    for key, value in warrior_data.items():
        setattr(db_warrior, key, value)
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior