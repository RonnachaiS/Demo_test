import os
import json
import re
from sqlmodel import Session, create_engine
from dotenv import load_dotenv
from main import News

# ตั้งค่า Database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# วางข้อมูล JSON ทั้งก้อนที่คุณก๊อปมาลงในตัวแปรนี้ครับ
wp_json_data = """
[ใส่ข้อมูล JSON ที่คุณส่งมาทั้งหมดตรงนี้ครับ ตั้งแต่ [{"id":10568,... จนจบ]
"""

def clean_html(raw_html):
    # ฟังก์ชันลบแท็ก HTML ให้เหลือแต่ข้อความ
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # ลบช่องว่างหรือรหัสแปลกๆ (เช่น &nbsp;)
    cleantext = cleantext.replace('&nbsp;', ' ').replace('\u201c', '"').replace('\u201d', '"').replace('\u2019', "'")
    return cleantext.strip()

def import_data():
    data = json.loads(wp_json_data)
    
    with Session(engine) as session:
        print(f"พบข้อมูลข่าวทั้งหมด {len(data)} บทความ กำลังเริ่มอิมพอร์ต...")
        
        for item in data:
            title = item['title']['rendered'].replace('&#8217;', "'").replace('&#8211;', "-")
            
            # ดึงเนื้อหาและสกัด HTML ออก
            raw_content = item['content']['rendered']
            content_text = clean_html(raw_content)
            
            # ค้นหา URL รูปภาพแรกในเนื้อหาด้วย Regex (ถ้ามี)
            img_match = re.search(r'src="([^"]+)"', raw_content)
            if img_match:
                image_url = img_match.group(1)
            else:
                image_url = "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=800&auto=format&fit=crop" # รูปสำรอง
                
            print(f"กำลังเพิ่ม: {title}")
            
            # สร้างข้อมูลลง Database
            news_entry = News(
                title=title,
                content=content_text,
                image_url=image_url
            )
            session.add(news_entry)
            
        session.commit()
        print("✅ ดึงข้อมูลข่าวจาก WordPress สำเร็จ 100%!")

if __name__ == "__main__":
    # ระวัง: เอา JSON วางตรงตัวแปร wp_json_data ก่อนรันด้วยนะครับ
    import_data()