from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from openai import OpenAI

# ======================
# INIT
# ======================
app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ======================
# AI FUNCTION (AMAN)
# ======================
def call_ai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error AI: {str(e)}"

# ======================
# ROUTES
# ======================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": ""}
    )

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    tool: str = Form(...),
    input1: str = Form(""),
    input2: str = Form(""),
    input3: str = Form(""),
    input4: str = Form("")
):
    if tool == "prompt_jualan":
        prompt = f"""
Kamu adalah copywriter profesional.

Produk: {input1}
Target market: {input2}
Masalah utama: {input3}
Platform: {input4}

Buatkan:
- 3 hook kuat
- 1 copy jualan singkat
- 1 CTA soft selling
Bahasa Indonesia.
"""

    elif tool == "auto_konten":
        prompt = f"""
Buatkan 15 ide konten.

Niche: {input1}
Platform: {input2}
Tujuan: {input3}
Gaya: {input4}

Format:
- Judul
- Caption
- CTA
"""

    elif tool == "auto_desain":
        prompt = f"""
Buatkan konsep desain promosi.

Produk: {input1}
Jenis desain: {input2}
Target market: {input3}
Tone: {input4}

Hasilkan:
- Judul
- Subjudul
- Bullet point
- CTA
"""

    elif tool == "riset_produk":
        prompt = f"""
Analisa niche {input1}.

Platform target: {input2}
Budget target: {input3}

Cari:
- Masalah utama market
- Produk potensial
- Range harga
- Ide produk digital turunan
"""

    else:
        prompt = "Tool tidak valid."

    result = call_ai(prompt)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )