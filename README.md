# propbot-william-properti
tugas hactivi8
# 🏠 PROPBOT — William Properti RAG Chatbot

Chatbot berbasis AI untuk agen properti William, membantu calon pembeli menemukan properti impian di Jawa Barat.

## 📌 Use Case
Customer service bot untuk agen properti — customer bisa tanya langsung ke AI tentang daftar properti, harga, cicilan, dan lokasi tanpa perlu menghubungi agen secara manual.

## 🧠 Arsitektur
PDF Katalog Properti → Chunking → Embedding (Gemini) → ChromaDB
User tanya → Retriever → Prompt → Gemini LLM → Jawaban
## ⚙️ Teknologi
- **LLM**: Google Gemini 2.5 Flash Lite
- **Embedding**: Google Gemini Embedding 2
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
- **Deployment**: Google Colab + ngrok

## 🚀 Cara Menjalankan
1. Buka `propbot_william_properti.ipynb` di Google Colab
2. Tambahkan secrets di Colab: `GEMINI` dan `NGROK_TOKEN`
3. Jalankan semua cell secara berurutan
4. Buka URL ngrok yang muncul di Cell 6

## 📋 Parameter Kreatif
- Gaya bahasa ramah dan profesional dalam Bahasa Indonesia
- Domain khusus properti Jawa Barat
- RAG untuk akurasi data katalog
- Quick suggestion buttons untuk kemudahan customer
- Tema UI luxury real estate (hitam & emas)

## 📁 File
- `propbot_william_properti.ipynb` — notebook utama (Google Colab)
- `propbot_app.py` — Streamlit UI
- `Katalog_Properti_Jabar_William.pdf` — data katalog properti
