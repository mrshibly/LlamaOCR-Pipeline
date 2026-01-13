# 📄 Bangla-English Document AI Pipeline

[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

A professional-grade Document AI pipeline that extracts structured information (Names, NID, DOB, Address) from scanned Bangla and English documents using **PaddleOCR** and **Llama 3 (via Groq)**.

## 🚀 Overview

This project provides an end-to-end solution for digitizing identification documents. It combines traditional computer vision (OpenCV), state-of-the-art OCR (PaddleOCR), and Large Language Models (LLMs) to transform messy document images into clean, structured JSON data.

### Key Features:
- **Hybrid OCR**: High-accuracy recognition for both Bangla and English scripts.
- **LLM-Powered Extraction**: Uses Llama 3 (Groq) to understand document semantics and extract names/addresses.
- **Interactive UI**: A sleek, glassmorphism-inspired web interface built with Tailwind CSS.
- **Dockerized**: Fully containerized and ready for deployment on Hugging Face Spaces or AWS/GC.

---

## 🏗️ Architecture

```mermaid
graph TD
    User([User]) -->|Upload Image| WebUI[Web Interface]
    WebUI -->|POST /extract| API[FastAPI Backend]
    
    subgraph "Processing Pipeline"
        API -->|1. Grayscale & Otsu| CV2[OpenCV Preprocessing]
        CV2 -->|2. Multilingual OCR| OCR[PaddleOCR Engine]
        OCR -->|3. Raw Text| Regex[Regex Fast-Extraction]
        Regex -->|4. Semantic Context| LLM[Groq Llama-3 API]
    end
    
    LLM -->|Structured JSON| API
    API -->|Final Response| WebUI
```

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **OCR Engine**: PaddleOCR (PaddlePaddle)
- **Image Processing**: OpenCV, NumPy
- **LLM Integration**: Groq SDK (Llama 3.3 70B)
- **Frontend**: HTML5, Tailwind CSS
- **Deployment**: Docker, Hugging Face Spaces

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/document-ai-pipeline.git
cd document-ai-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
# Set your Groq API Key
export GROQ_API_KEY="your_api_key_here"
```

### 4. Run Locally
```bash
python app.py
```
Access the app at `http://localhost:7860`.

---

## 🐳 Docker Deployment

To build and run the container locally:
```bash
docker build -t document-ai .
docker run -p 7860:7860 -e GROQ_API_KEY="your_api_key" document-ai
```

---

## 📂 Project Structure
- `app.py`: Core FastAPI application and logic.
- `index.html`: Interactive frontend.
- `notebooks/`: Research and development exploration.
- `samples/`: Example document images for testing.
- `Dockerfile`: Container configuration.
- `requirements.txt`: Python package list.

---

## 👨‍💻 Author
**Your Name**
*Software Engineer | AI Enthusiast*
[LinkedIn](your-linkedin-url) | [Portfolio](your-portfolio-url)
