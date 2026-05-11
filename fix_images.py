import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv
from main import News

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def force_fix_images():
    with Session(engine) as session:
        # ดึงข่าวทั้งหมดออกมา
        news_list = session.exec(select(News)).all()
        
        # ลิงก์รูปภาพที่ทดสอบแล้วว่าโหลดได้ชัวร์ 100%
        working_images = [
            "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80", # รูปรถสีขาว (รูปแรกที่โหลดผ่าน)
            "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80", # รูปรถ Ferrari
            "https://images.unsplash.com/photo-1503376762364-74971d604e13?auto=format&fit=crop&w=800&q=80"  # รูปรถ Porsche
        ]

        # วนลูปอัปเดตทุกข่าวในระบบ (ใช้ % เพื่อให้รูปวนซ้ำถ้ามีข่าวมากกว่า 3 อัน)
        for i, news in enumerate(news_list):
            news.image_url = working_images[i % len(working_images)]
            session.add(news)
        
        session.commit()
        print("✅ อัปเดต URL รูปภาพใหม่สำเร็จแล้ว!")

if __name__ == "__main__":
    force_fix_images()