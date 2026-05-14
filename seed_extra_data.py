import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv
from main import Biography, Gallery, Service

# เชื่อมต่อ Database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# ==========================================
# 1. ข้อมูลประวัติการแข่งจริงของ Sandy Stuvik
# ==========================================
bio_data = [
    {
        "year": 2025,
        "championship": "Thailand Super Series (GT3 & Super Pickup)",
        "car": "Porsche 992 GT3 R / Ford Ranger",
        "details": "Competing for the championship with B-Quik Absolute Racing and Ford Thailand Racing."
    },
    {
        "year": 2022,
        "championship": "Thailand Super Series GT3 - Overall Champion",
        "car": "Audi R8 LMS GT3 Evo II",
        "details": "Secured his 3rd overall Thailand Super Series GT3 Championship title."
    },
    {
        "year": 2020,
        "championship": "Thailand Super Series GT3 - Overall Champion",
        "car": "Audi R8 LMS GT3 Evo",
        "details": "Back-to-back championship victory despite a challenging pandemic-shortened season."
    },
    {
        "year": 2019,
        "championship": "Thailand Super Series GT3 - Overall Champion",
        "car": "Audi R8 LMS GT3",
        "details": "First GT3 championship title in Thailand, showcasing dominant pace."
    },
    {
        "year": 2014,
        "championship": "Euroformula Open Championship - Champion",
        "car": "Dallara F312 (Formula 3)",
        "details": "Dominant season in Europe, securing 11 wins and setting a record for the series."
    },
    {
        "year": 2010,
        "championship": "Asian Formula Renault Challenge - Champion",
        "car": "Formula Renault 2.0",
        "details": "First major championship win in his early single-seater career."
    }
]

# ==========================================
# 2. ข้อมูลรูปภาพ Gallery (ใช้รูปจำลองความละเอียดสูงแนว Racing)
# ==========================================
gallery_data = [
    {"title": "GT3 Action at Buriram", "category": "Racing", "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80"},
    {"title": "Podium Celebration", "category": "Podium", "image_url": "https://images.unsplash.com/photo-1534142498207-6950e322cd81?auto=format&fit=crop&w=800&q=80"},
    {"title": "Pitlane Focus", "category": "Behind the Scenes", "image_url": "https://images.unsplash.com/photo-1610884447640-42b8ec61a933?auto=format&fit=crop&w=800&q=80"},
    {"title": "Rain Race Masterclass", "category": "Racing", "image_url": "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?auto=format&fit=crop&w=800&q=80"},
    {"title": "Ford Ranger Super Pickup", "category": "Racing", "image_url": "https://images.unsplash.com/photo-1559416523-140ddc3d238c?auto=format&fit=crop&w=800&q=80"},
    {"title": "Simulator Training", "category": "Training", "image_url": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=800&q=80"}
]

# ==========================================
# 3. ข้อมูล Services / Private Coaching
# ==========================================
services_data = [
    {
        "name": "Private Track Coaching",
        "description": "1-on-1 in-car coaching tailored to improve your lap times, braking points, and racecraft at circuits across Asia.",
        "price_info": "Contact for Pricing",
        "image_url": "https://images.unsplash.com/photo-1541348263662-e068f6284564?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Pro Simulator Training",
        "description": "Advanced simulator sessions to learn new tracks, perfect your driving technique, and build muscle memory safely.",
        "price_info": "Starting from ฿5,000/hr",
        "image_url": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Corporate Track Days",
        "description": "Exclusive motorsport experiences for corporate clients. Thrill your VIPs with a hot lap alongside a 3-time TSS Champion.",
        "price_info": "Custom Packages",
        "image_url": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Sandy Drives (Car Review)",
        "description": "Professional testing, feedback, and video reviews for automotive brands looking for a professional racing driver's insight.",
        "price_info": "Contact for Details",
        "image_url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=800&q=80"
    }
]

def run_seed():
    with Session(engine) as session:
        print("⏳ กำลังล้างข้อมูลเก่า และอัปเดตข้อมูลใหม่...")
        
        # 1. จัดการ Biography
        existing_bio = session.exec(select(Biography)).all()
        if not existing_bio:
            for b in bio_data:
                session.add(Biography(**b))
            print("✅ เพิ่ม Biography สำเร็จ")
        
        # 2. จัดการ Gallery
        existing_gal = session.exec(select(Gallery)).all()
        if not existing_gal:
            for g in gallery_data:
                session.add(Gallery(**g))
            print("✅ เพิ่ม Gallery สำเร็จ")
            
        # 3. จัดการ Services
        existing_svc = session.exec(select(Service)).all()
        if not existing_svc:
            for s in services_data:
                session.add(Service(**s))
            print("✅ เพิ่ม Services สำเร็จ")

        session.commit()
        print("🎉 สร้างข้อมูลพื้นฐานเสร็จสมบูรณ์!")

if __name__ == "__main__":
    run_seed()