import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv
from main import Product

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def seed_shop():
    products = [
        Product(
            name="Sandy Stuvik Official Cap 2024",
            price=950.0,
            description="Limited Edition official racing cap with 3D embroidery logo.",
            image_url="https://m.media-amazon.com/images/I/71Yv8y6D8mL._AC_SL1500_.jpg" # ตัวอย่างรูปหมวก
        ),
        Product(
            name="TSS Champion Polo Shirt",
            price=1250.0,
            description="Premium breathable fabric with sponsor logos and 3x Champion patch.",
            image_url="https://m.media-amazon.com/images/I/61K7z1m-RLL._AC_SL1500_.jpg" # ตัวอย่างรูปเสื้อโปโล
        ),
        Product(
            name="Racing Team T-Shirt (Black)",
            price=790.0,
            description="100% Cotton with high-quality screen print design.",
            image_url="https://m.media-amazon.com/images/I/61M6Yh9Wn+L._AC_SL1500_.jpg" # ตัวอย่างรูปเสื้อยืด
        )
    ]
    
    with Session(engine) as session:
        # ล้างข้อมูลเก่า (ถ้ามี)
        existing = session.exec(select(Product)).all()
        for p in existing: session.delete(p)
        
        for p in products: session.add(p)
        session.commit()
    print("✅ เพิ่มสินค้าใน Shop สำเร็จ!")

if __name__ == "__main__":
    seed_shop()