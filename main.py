import os
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env (สำหรับตอนรันในเครื่อง)
load_dotenv()

# ดึง Connection String มาใช้
DATABASE_URL = os.getenv("DATABASE_URL")

# สร้าง Engine สำหรับต่อ Database
engine = create_engine(DATABASE_URL, echo=True)

class News(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    image_url: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sandy Stuvik Web Demo")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Sandy Stuvik Demo API"}

@app.get("/api/news")
def get_news():
    with Session(engine) as session:
        news = session.exec(select(News)).all()
        return news