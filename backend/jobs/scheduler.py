from apscheduler.schedulers.background import BackgroundScheduler
from scraping.simo_scraping_playwright import scraping_simo
from backend.schemas import Empleo
import json
from datetime import datetime

empleos_guardados = []

def guardar_empleos_periodicamente():
    print(f"[{datetime.now()}] Iniciando scraping programado...")
    try:
        empleos = asyncio.run(scraping_simo())
        global empleos_guardados
        empleos_guardados = empleos
        with open("empleos_diarios.json", "w", encoding="utf-8") as f:
            json.dump([e.dict() for e in empleos], f, ensure_ascii=False, indent=2)
        print(f"[{datetime.now()}] Empleos actualizados: {len(empleos)}")
    except Exception as e:
        print(f"[ERROR] Scraping fallido: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(guardar_empleos_periodicamente, 'cron', hour='6,18', minute=0)  # 6:00 y 18:00
    scheduler.start()
