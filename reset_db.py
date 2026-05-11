import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv
from main import News

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def reset_and_fix_db():
    with Session(engine) as session:
        # 1. ลบข้อมูลข่าวเก่าทั้งหมดทิ้งก่อน เพื่อความคลีน
        old_news = session.exec(select(News)).all()
        for news in old_news:
            session.delete(news)
        session.commit()

        # 2. เพิ่มข้อมูลใหม่ 3 ข่าว พร้อม URL รูปภาพที่ทดสอบแล้ว
        fresh_news = [
            News(
                title="Strong Finish for Sandy at TSS 2025 Finale",
                content="The final round of the Thailand Super Series 2025 saw Sandy Kraokaew Stuvik close out the season with two solid results at the wheel of the B-Quik Absolute Racing #26 Porsche 911 GT3 R.",
                image_url="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=800&auto=format&fit=crop" # รูป 1: รถสีขาว
            ),
            News(
                title="Sandy Kraokaew Stuvik Takes Emotional Victory for Ford Thailand Racing",
                content="It was a weekend of highs and lows for Sandy Kraokaew Stuvik and Ford Thailand Racing, as the Thailand Super Series concluded its 2025 season at the Chang International Circuit.",
                image_url="https://images.unsplash.com/photo-1583121274602-3e2820c69888?q=80&w=800&auto=format&fit=crop" # รูป 2: รถ Ferrari สีแดง
            ),
            News(
                title="Sandy Kraokaew Stuvik Set for Final Round of TSS 2025",
                content="Thai racing driver Sandy Kraokaew Stuvik is gearing up for the final round of the 2025 Thailand Super Series, taking place at the renowned Chang International Circuit in Buriram.",
                image_url="https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=800&auto=format&fit=crop" # รูป 3: รถสปอร์ตสีดำ
            )
        ]
        
        for news in fresh_news:
            session.add(news)
        
        session.commit()
        print("✅ ล้างข้อมูลและใส่รูปใหม่สำเร็จ!")

if __name__ == "__main__":
    reset_and_fix_db()