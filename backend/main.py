
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from backend.routes import empleos

load_dotenv()
app = FastAPI(title="API Empleos SIMO")
app.include_router(empleos.router)

@app.get("/")
async def root():
    return {"message": "API de scraping SIMO activa"}
