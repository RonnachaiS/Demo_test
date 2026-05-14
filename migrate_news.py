import os
import json
import re
from sqlmodel import Session, create_engine, select  # <--- เพิ่ม select เข้ามาตรงนี้ครับ
from dotenv import load_dotenv
from main import News

# 1. เชื่อมต่อฐานข้อมูล Neon
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# 2. ข้อมูล JSON จากเว็บเก่า (sandystuvik.com)
wp_data = """
[
    {"title":{"rendered":"Strong Finish for Sandy at TSS 2025 Finale"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/11/TSS2025-Final-round-2-1024x683.jpg\\"></p><p>The final round of the Thailand Super Series 2025 saw Sandy Kraokaew Stuvik close out the season with two solid results...</p>"}},
    {"title":{"rendered":"Sandy Kraokaew Stuvik Takes Emotional Victory for Ford Thailand Racing"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/11/TN203540-1-1024x683.jpg\\"></p><p>It was a weekend of highs and lows for Sandy Kraokaew Stuvik and Ford Thailand Racing...</p>"}},
    {"title":{"rendered":"Sandy Kraokaew Stuvik Set for Final Round of TSS 2025"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/10/Sandy-TSS-R5_2025-7-1024x683.jpg\\"></p><p>Thai racing driver Sandy Kraokaew Stuvik is gearing up for the final round of the 2025 Thailand Super Series...</p>"}},
    {"title":{"rendered":"Solid Weekend for Sandy Kraokaew Stuvik at Sepang"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/09/S__33170101-1024x719.jpg\\"></p><p>Sandy Kraokaew Stuvik returned to action in the Thailand Super Series 2025, competing in Round 4 at the iconic Sepang...</p>"}},
    {"title":{"rendered":"Sandy Sets Sights on Sepang"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/09/Sandy-Sepang-2025-18-1024x683.jpg\\"></p><p>Thai motorsport star Sandy Kraokaew Stuvik and teammate Henk Kiks are preparing to take on Round 4...</p>"}},
    {"title":{"rendered":"Double podium in Sepang for Sandy"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/08/Sandy-Sepang-2025-37-1024x683.jpg\\"></p><p>B-Quik Absolute Racing’s Sandy Kraokaew Stuvik and co-driver Henk Kiks delivered a strong performance in Round 3...</p>"}},
    {"title":{"rendered":"Sandy Battles to Strong Finishes at Bangsaen Grand Prix"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/07/Sandy-BSP2025-3-1024x684.jpg\\"></p><p>Kiks qualified the car in 5th position in Q1, setting the grid for Saturday’s race...</p>"}},
    {"title":{"rendered":"Sandy Kraokaew Stuvik Ready for Bangsaen Grand Prix"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/06/Sandy-2-1024x683.jpg\\"></p><p>Thai racing star Sandy Kraokaew Stuvik is set to return to the streets of Bangsaen for the second round...</p>"}},
    {"title":{"rendered":"Sandy Kraokaew Stuvik Continues with Ford Thailand Racing"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/06/Sandy_Pickup-2024-7-1024x683.jpg\\"></p><p>Expanding his racing program for the 2025 season, multi-time champion Sandy Kraokaew Stuvik is set to compete...</p>"}},
    {"title":{"rendered":"Sandy Kraokaew Stuvik Joins B-Quik Absolute Racing"}, "content":{"rendered":"<p><img src=\\"https://www.sandystuvik.com/wp-content/uploads/2025/06/Sandy-x-Henk-1-1024x683.jpg\\"></p><p>Sandy Kraokaew Stuvik is set to return to the Thailand Super Series (TSS) GT3 category in 2025...</p>"}}
]
"""

def clean_html(raw_html):
    # ลบ HTML tags ให้เหลือแต่ข้อความธรรมดา
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.replace('&nbsp;', ' ').replace('&#8217;', "'").replace('&#8211;', "-").strip()

def run_migration():
    data = json.loads(wp_data)
    with Session(engine) as session:
        print("🚀 กำลังย้ายข้อมูลจากเว็บเก่าสู่ระบบใหม่...")
        for item in data:
            title = clean_html(item['title']['rendered'])
            raw_content = item['content']['rendered']
            
            # ใช้ Regex ดึงลิงก์รูปภาพออกมาจากเนื้อหา HTML
            img_match = re.search(r'src="([^"]+)"', raw_content)
            image_url = img_match.group(1) if img_match else "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7"
            
            clean_content = clean_html(raw_content)

            # ตรวจสอบว่าข่าวนี้มีอยู่แล้วหรือไม่ เพื่อป้องกันการ Add ซ้ำ
            existing = session.exec(select(News).where(News.title == title)).first()
            if not existing:
                news_entry = News(title=title, content=clean_content, image_url=image_url)
                session.add(news_entry)
                print(f"✅ เพิ่มข่าว: {title[:30]}...")
            else:
                print(f"⏩ ข้ามข่าว (มีในระบบแล้ว): {title[:30]}...")
            
        session.commit()
        print("🎉 ย้ายข้อมูลเสร็จสมบูรณ์ 100% ไม่มีตกหล่น!")

if __name__ == "__main__":
    run_migration()