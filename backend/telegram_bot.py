import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request


# Cargar variables de entorno desde .env automáticamente
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "<TU_TOKEN_AQUI>")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


# Estado de conversación por usuario (en memoria, para demo)
user_states = {}

app = FastAPI()

# Webhook endpoint para Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    print("[DEBUG] Mensaje recibido:", data)
    chat_id = str(data["message"]["chat"]["id"])
    text = data["message"].get("text", "").strip()
    state = user_states.get(chat_id, {})
    # Inicio de conversación
    if text.lower() == "/start" or not state:
        filtros = requests.get(f"{BACKEND_URL}/empleos/opciones-filtros").json()
        departamentos = filtros.get("departamentos", [])
        keyboard = [[d] for d in departamentos[:20]]  # Solo los primeros 20 para no saturar
        reply = "¿En qué departamento deseas buscar empleo?"
        user_states[chat_id] = {"step": "departamento", "filtros": filtros}
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply,
            "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}
        })
        print("[DEBUG] Pregunta departamento enviada.")
        return JSONResponse({"ok": True})
    # Selección de departamento
    if state.get("step") == "departamento":
        filtros = state["filtros"]
        if text not in filtros.get("departamentos", []):
            reply = "Por favor selecciona un departamento válido."
            requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
            return JSONResponse({"ok": True})
        ciudades = filtros.get("ciudades", [])
        keyboard = [[c] for c in ciudades[:20]]
        user_states[chat_id]["departamento"] = text
        user_states[chat_id]["step"] = "ciudad"
        reply = f"¿En qué ciudad de {text} deseas buscar?"
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply,
            "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}
        })
        print("[DEBUG] Pregunta ciudad enviada.")
        return JSONResponse({"ok": True})
    # Selección de ciudad
    if state.get("step") == "ciudad":
        filtros = state["filtros"]
        if text not in filtros.get("ciudades", []):
            reply = "Por favor selecciona una ciudad válida."
            requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
            return JSONResponse({"ok": True})
        user_states[chat_id]["ciudad"] = text
        user_states[chat_id]["step"] = "salario"
        reply = "¿Cuál es el salario mínimo que buscas? (puedes escribir solo el número o dejar vacío)"
        keyboard = [["/omitir"]]
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply,
            "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}
        })
        print("[DEBUG] Pregunta salario enviada.")
        return JSONResponse({"ok": True})
    # Salario mínimo
    if state.get("step") == "salario":
        if text == "/omitir":
            salario_min = None
        else:
            salario_min = int(text) if text.isdigit() else None
        user_states[chat_id]["salario_min"] = salario_min
        user_states[chat_id]["step"] = "final"
        reply = "¿Deseas filtrar por OPEC, propósito, profesión o estudios? Si sí, escribe el valor, si no, responde 'no' o pulsa /omitir."
        keyboard = [["/omitir"]]
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply,
            "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}
        })
        print("[DEBUG] Pregunta filtro extra enviada.")
        return JSONResponse({"ok": True})
    # Filtro final y consulta
    if state.get("step") == "final":
        filtros = {
            "departamento": user_states[chat_id].get("departamento"),
            "ciudad": user_states[chat_id].get("ciudad"),
            "salario_min": user_states[chat_id].get("salario_min"),
        }
        if text.lower() not in ["no", "/omitir"]:
            if text.isdigit():
                filtros["numero_opec"] = text
            else:
                filtros["profesion"] = text
        resp = requests.post(f"{BACKEND_URL}/telegram/consulta", params={"mensaje": ""}, json=filtros)
        empleos = resp.json()
        if not empleos:
            reply = "No se encontraron empleos activos para tu consulta."
        else:
            reply = "\n\n".join([
                f"{e.get('titulo','')}\nEntidad: {e.get('entidad','')}\nCiudad: {e.get('municipio','')}\nSalario: {e.get('asignacion_salarial','')}\nCierre: {e.get('fecha_cierre','')}" for e in empleos[:5]
            ])
            if len(empleos) > 5:
                reply += f"\n\nY {len(empleos)-5} más..."
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
        print("[DEBUG] Respuesta enviada:", reply[:400])
        user_states.pop(chat_id, None)
        return JSONResponse({"ok": True})
    # Si no hay estado válido, reiniciar
    reply = "Por favor inicia con /start para buscar empleos."
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return JSONResponse({"ok": True})

# Utilidad para registrar el webhook en Telegram
if __name__ == "__main__":
    # Cambia la URL por la de tu servidor en producción
    webhook_url = os.getenv("WEBHOOK_URL", "https://tu-servidor.com/webhook")
    r = requests.get(f"{API_URL}/setWebhook", params={"url": webhook_url})
    print(r.json())
