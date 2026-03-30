import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v27.2 - HATTU ONAR (YENİ URL & TABLO ENTEGRASYONU)
st.set_page_config(page_title="Erkoz Analiz v27.2", layout="wide", page_icon="🚴‍♂️")

# --- GÜNCEL AYARLAR ---
ADMIN_PASSWORD = "erkoz" 
# Senin verdiğin yeni Apps Script URL'si:
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UZvqPnAzqiFfdUFGuKmvHQKPjsNC3gDHNYO5KO0yOgIq_737ST5_5yEDa5UNz7guobg/exec"
# Google Sheets (Excel) dosyanın kendi linki:
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (PROFİL & KONTROL PANELİ) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım & Performans")
bisiklet_markasi = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme (1-3)", [1, 2, 3], index=2)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Alanı")
sifre_denemesi = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Yönetici Panelini Aç"):
    if sifre_denemesi == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("Panel Aktif!")
    else:
        st.sidebar.error("Hatalı Şifre!")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Terminali")

if st.session_state.is_admin:
    st.markdown("### 🛠️ Yönetici Kontrol Paneli")
    # Tabloyu aç butonu burada güncellendi
    st.markdown(f"""
        <a href="{SHEETS_LINK}" target="_blank">
            <button style="width:100%; height:60px; background-color:#FF4B4B; color:white; border:none; border-radius:12px; font-weight:bold; font-size:18px; cursor:pointer;">
                📊 GÜNCEL EXCEL TABLOSUNU GÖRÜNTÜLE
            </button>
        </a>
    """, unsafe_allow_html=True)
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.is_admin = False
        st.rerun()

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Verileri")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=157.0)
    kalori = st.number_input("Yakılan Kalori (kcal)", value=3150)
with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    yukselti = st.number_input("Tırmanış (m)", value=1049)

# --- ANALİZ VE KAYIT ---
if st.button("🚀 SÜRÜŞÜ ANALİZ ET VE EXCEL'E GÖNDER"):
    # Puan Hesaplama Formülü
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    std_puan = round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + (vke / 5), 3)
    km_p = round((std_puan / surus_km) * 100, 3)
    rz_p = round((km_p / 10) * kademe, 3)
    yk_p = round((yukselti / 1000 * 0.3) + 1, 3)
    final_puan = round(km_p + rz_p + yk_p, 3)

    # 8 Sütunlu Tam Hizalanmış Veri Paketi
    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": bisiklet_markasi, 
        "bisKilosu": bisiklet_kilosu,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        # Yeni URL üzerinden gönderim
        response = requests.post(SCRIPT_URL, json=payload)
        if response.status_code == 200:
            st.balloons()
            st.success("✅ Veriler yeni köprü üzerinden başarıyla Excel'e işlendi!")
            
            # BAŞARI BELGESİ
            st.markdown(f"""
            <div style="background:#0E1117; border:5px double #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center;">
                <h2 style="color:#FF4B4B; margin-top:0;">🏆 ERKOZ BAŞARI BELGESİ</h2>
                <p style="font-size:18px;"><b>{ad_soyad}</b></p>
                <hr style="border:0.5px solid #333;">
                <h1 style="color:#FF4B4B; font-size:60px; margin:10px 0;">{final_puan}</h1>
                <p>{surus_km} KM | {yukselti} M | {ruzgar_hizi} km/h</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Sunucu hatası: {response.status_code}")
    except Exception as e:
        st.error(f"Bağlantı kurulamadı: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
