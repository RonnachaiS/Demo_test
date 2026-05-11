import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

class News(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    image_url: str

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    description: str
    image_url: str

# 1. เพิ่ม Table สำหรับเก็บข้อมูลออเดอร์
class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    address: str
    payment_method: str
    total_amount: float
    status: str = Field(default="Pending Review") # สถานะรอตรวจสอบสลิป

# 2. เพิ่ม Model รับข้อมูลจาก Frontend
class OrderCreate(BaseModel):
    customer_name: str
    address: str
    payment_method: str
    total_amount: float
    cart_items: list

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sandy Stuvik Web Demo")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/news")
def get_news():
    with Session(engine) as session:
        return session.exec(select(News)).all()

@app.get("/api/products")
def get_products():
    with Session(engine) as session:
        return session.exec(select(Product)).all()

# 3. เพิ่ม API สำหรับรับออเดอร์ใหม่
@app.post("/api/orders")
def create_order(order_data: OrderCreate):
    with Session(engine) as session:
        new_order = Order(
            customer_name=order_data.customer_name,
            address=order_data.address,
            payment_method=order_data.payment_method,
            total_amount=order_data.total_amount
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return {"message": "Order placed successfully", "order_id": new_order.id, "status": new_order.status}