from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil
import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
import unicodedata
import re
import requests
import json
from groq import Groq

app = FastAPI()

# 🧠 Singleton OCR & LLM Initialization
ocr = PaddleOCR(use_angle_cls=True, lang='bn', use_gpu=False, ocr_version='PP-OCRv3')
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def run_ocr(image):
    result = ocr.ocr(image, cls=True)
    text_lines = [line[1][0] for line in result[0]] if (result and result[0]) else []
    return unicodedata.normalize("NFKC", "\n".join(text_lines))

def extract_info(text):
    data = {}
    # Regex as fallback/fast extraction
    nid_match = re.search(r'(\d{10}|\d{13}|\d{17})', text)
    if nid_match: data['nid_number'] = nid_match.group(1)
    
    date_match = re.search(r'(\d{2}[-/\.]\d{2}[-/\.]\d{4})', text)
    if date_match: data['date_of_birth'] = date_match.group(1)
    
    # --- Groq LLM Extraction ---
    if not os.environ.get("GROQ_API_KEY"):
        data['error'] = "GROQ_API_KEY not set. Using basic regex extraction."
        return data

    prompt = f"""Extract Name, Father's Name, Mother's Name, and Address from the following OCR text.
    Text:
    {text}
    
    Return the result in strictly valid JSON format with keys: 'name', 'father_name', 'mother_name', 'address'.
    If a field is not found, use "Not Found" as the value."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        llm_data = json.loads(completion.choices[0].message.content)
        data.update(llm_data)
    except Exception as e:
        data['llm_error'] = str(e)
    
    return data

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/extract")
async def api_extract(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        clean = preprocess_image(img)
        text = run_ocr(clean)
        structured = extract_info(text)
        
        return {"status": "success", "structured_data": structured, "raw_text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860) # Port 7860 is default for HF Spaces
