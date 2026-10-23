# main.py
from fastapi import FastAPI
from src.database.db import engine
from src.database.models import Base

Base.metadata.create_all(bind=engine)

from src.routes import skills
from src.routes import users

app = FastAPI(title="SkillSwap API",
              description="Desc",
              version="1.0.0")

app.include_router(skills.router)
app.include_router(users.router)

@app.get("/health")
def read_root():
    return {"message": "test main root"}
