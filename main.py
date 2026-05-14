import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# ==========================================
# 1. DATABASE MODELS
# ==========================================
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

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    address: str
    payment_method: str
    total_amount: float
    status: str = Field(default="Pending") 

class Biography(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int
    championship: str
    car: str
    details: str

class Gallery(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    image_url: str
    category: str

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price_info: str
    image_url: str

class ContactMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    message: str

# ==========================================
# 2. PYDANTIC MODELS (รับข้อมูลจาก Frontend)
# ==========================================
class OrderCreate(BaseModel):
    customer_name: str
    address: str
    payment_method: str
    total_amount: float
    cart_items: list

class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class StatusUpdate(BaseModel):
    status: str

# ==========================================
# 3. APP SETUP
# ==========================================
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sandy Stuvik Web Demo")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ==========================================
# 4. FRONTEND ROUTES
# ==========================================
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# --- หน้า Admin ---
@app.get("/admin")
def read_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")

# ==========================================
# 5. API ROUTES (Public & Admin)
# ==========================================
# --- NEWS ---
@app.get("/api/news")
def get_news():
    with Session(engine) as session:
        return session.exec(select(News).order_by(News.id.desc())).all()

@app.post("/api/news")
def create_news(news: News):
    with Session(engine) as session:
        session.add(news)
        session.commit()
        return {"message": "News created"}

@app.delete("/api/news/{news_id}")
def delete_news(news_id: int):
    with Session(engine) as session:
        news = session.get(News, news_id)
        if not news: raise HTTPException(status_code=404, detail="News not found")
        session.delete(news)
        session.commit()
        return {"message": "News deleted"}

# --- PRODUCTS ---
@app.get("/api/products")
def get_products():
    with Session(engine) as session:
        return session.exec(select(Product).order_by(Product.id.desc())).all()

@app.post("/api/products")
def create_product(prod: Product):
    with Session(engine) as session:
        session.add(prod)
        session.commit()
        return {"message": "Product created"}

@app.delete("/api/products/{prod_id}")
def delete_product(prod_id: int):
    with Session(engine) as session:
        prod = session.get(Product, prod_id)
        if not prod: raise HTTPException(status_code=404, detail="Product not found")
        session.delete(prod)
        session.commit()
        return {"message": "Product deleted"}

# --- ORDERS ---
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

@app.get("/api/orders")
def get_all_orders():
    with Session(engine) as session:
        return session.exec(select(Order).order_by(Order.id.desc())).all()

@app.put("/api/orders/{order_id}")
def update_order_status(order_id: int, status_update: StatusUpdate):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order: raise HTTPException(status_code=404, detail="Order not found")
        order.status = status_update.status
        session.add(order)
        session.commit()
        return {"message": "Status updated"}

# --- OTHER GET ROUTES ---
@app.get("/api/biography")
def get_biography():
    with Session(engine) as session:
        return session.exec(select(Biography).order_by(Biography.year.desc())).all()

@app.get("/api/gallery")
def get_gallery():
    with Session(engine) as session:
        return session.exec(select(Gallery)).all()

@app.get("/api/services")
def get_services():
    with Session(engine) as session:
        return session.exec(select(Service)).all()

@app.post("/api/contact")
def create_contact_message(contact_data: ContactCreate):
    with Session(engine) as session:
        new_msg = ContactMessage(
            name=contact_data.name, email=contact_data.email,
            subject=contact_data.subject, message=contact_data.message
        )
        session.add(new_msg)
        session.commit()
        return {"message": "Message sent"}