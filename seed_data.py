import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv

# นำเข้า Model News จากไฟล์ main.py
from main import News

# โหลด Environment Variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# ข้อมูลจริงที่ดึงมาจาก www.sandystuvik.com
real_news_data = [
    {
        "title": "Strong Finish for Sandy at TSS 2025 Finale",
        "content": "The final round of the Thailand Super Series 2025 saw Sandy Kraokaew Stuvik close out the season with two solid results at the wheel of the B-Quik Absolute Racing #26 Porsche 911 GT3 R, sharing the driving duties with teammate Henk Kiks.",
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=800&auto=format&fit=crop" # รูปตัวอย่างรถแข่ง
    },
    {
        "title": "Sandy Kraokaew Stuvik Takes Emotional Victory for Ford Thailand Racing",
        "content": "It was a weekend of highs and lows for Sandy Kraokaew Stuvik and Ford Thailand Racing, as the Thailand Super Series concluded its 2025 season at the Chang International Circuit in Buriram. Competing in the #3 Ford Ranger in the Super Pickup class, Sandy showed remarkable pace.",
        "image_url": "https://images.unsplash.com/photo-1541348263662-e06836264b98?q=80&w=800&auto=format&fit=crop" # รูปตัวอย่างแชมเปญ/ชัยชนะ
    },
    {
        "title": "Sandy Kraokaew Stuvik Set for Final Round of TSS 2025",
        "content": "Thai racing driver Sandy Kraokaew Stuvik is gearing up for the final round of the 2025 Thailand Super Series, taking place at the renowned Chang International Circuit in Buriram on November 1–2.",
        "image_url": "https://images.unsplash.com/photo-1532981541460-64472d82582d?q=80&w=800&auto=format&fit=crop" # รูปตัวอย่างสนามแข่ง
    }
]

def seed_db():
    with Session(engine) as session:
        # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่ จะได้ไม่ใส่ซ้ำ
        existing_news = session.exec(select(News)).first()
        if existing_news:
            print("มีข้อมูลใน Database อยู่แล้ว ไม่จำเป็นต้องเพิ่มใหม่")
            return

        print("กำลังเพิ่มข้อมูลข่าวจากเว็บ sandystuvik.com ลงใน Database...")
        for data in real_news_data:
            news_item = News(**data)
            session.add(news_item)
        
        session.commit()
        print("เพิ่มข้อมูลสำเร็จเรียบร้อย!")

if __name__ == "__main__":
    seed_db()