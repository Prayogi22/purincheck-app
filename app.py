import streamlit as st
import google.generativeai as genai
from PIL import Image

# Masukkan API Key Gemini Anda di bawah ini
GEMINI_API_KEY = "AIzaSyAkB4uYdRe0CnWUvtOj13jISPaloofFO_c"
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="PurinCheck AI", page_icon="🥗", layout="centered")

# CSS custom agar tampilan di HP terlihat seperti aplikasi native
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 500px; padding-top: 1rem; }
    stButton>button { width: 100%; border-radius: 10px; height: 3rem; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🥗 PurinCheck AI")
st.write("Cek kadar purin makanan secara instan via teks atau foto kamera.")

menu = st.tabs(["📷 Ambil Foto", "✍️ Ketik Nama"])

prompt_instruksi = """
Anda adalah ahli gizi klinis spesialis asam urat. Analisis makanan/minuman berikut dan berikan jawaban ringkas di HP:
### 🍽️ [Nama Makanan]
#### 🚨 Risiko: [RISIKO TINGGI (DILARANG) / RISIKO SEDANG (BATASI) / AMAN (DIANJURKAN)] -> Berikan warna emoji sesuai risiko.
#### 📊 Purin: [Estimasi mg per 100g atau kategori tinggi/rendah]
#### 💡 Catatan singkat & Alternatif aman.
"""

with menu[0]:
    # Menggunakan camera_input agar otomatis menyalakan kamera HP
    foto_hp = st.camera_input("Foto makanan Anda:")
    if foto_hp:
        gambar = Image.open(foto_hp)
        if st.button("Cek Kandungan Purin 🔍", key="btn_foto"):
            with st.spinner("Menganalisis..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([prompt_instruksi, "Analisis foto ini", gambar])
                st.markdown(response.text)

with menu[1]:
    nama_makanan = st.text_input("Ketik nama makanan:", placeholder="Contoh: Emping, Sapi Lada Hitam")
    if nama_makanan:
        if st.button("Cek Kandungan Purin 🔍", key="btn_teks"):
            with st.spinner("Menganalisis..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([prompt_instruksi, f"Analisis makanan: {nama_makanan}"])
                st.markdown(response.text)
