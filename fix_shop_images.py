import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv
from main import Product

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def fix_shop_images():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        
        # ลิงก์รูปภาพที่ทดสอบแล้วว่าโหลดได้ (ใช้รูปหมวก และเสื้อยืดจาก Unsplash เป็นตัวอย่าง)
        working_images = [
            "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?auto=format&fit=crop&w=800&q=80", # รูปหมวกแก๊ป
            "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=800&q=80", # รูปเสื้อคอปก/เสื้อยืด
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80"  # รูปเสื้อยืดสีดำ
        ]

        # อัปเดต URL
        for i, product in enumerate(products):
            if i < len(working_images):
                product.image_url = working_images[i]
                session.add(product)
        
        session.commit()
        print("✅ แก้ไขรูปภาพสินค้าเรียบร้อยแล้ว!")

if __name__ == "__main__":
    fix_shop_images()