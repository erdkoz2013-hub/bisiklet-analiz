import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v27.5 - KESİNTİSİZ BAĞLANTI GÜNCELLEMESİ
st.set_page_config(page_title="Erkoz Analiz v27.5", layout="wide", page_icon="🚴‍♂️")

# --- YENİ AKTİF URL ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- YAN PANEL ---
st.sidebar.header("🔑 Yönetici Girişi")
sifre = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Giriş Yap"):
    if sifre == "erkoz":
        st.session_state.is_admin = True
        st.sidebar.success("Sistem hazır kanka!")
    else:
        st.sidebar.error("Hatalı!")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Terminali")
if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">📊 EXCEL TABLOSUNU (LİSTEYİ) AÇ</button></a>', unsafe_allow_html=True)

st.markdown("---")

# Veri Giriş Alanları
ad_soyad = st.text_input("Sürücü Adı Soyadı", value="Erdal Kozal")
col1, col2 = st.columns(2)
with col1:
    surus_km = st.number_input("Yapılan KM", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
with col2:
    yukselti = st.number_input("Tırmanış / Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())

# Arka Plan Hesaplamaları (Gizli Formül)
# Bu veriler Excel'e gitmez, sadece puanı etkiler
yas = 59 # Sabit hesaplama verisi
kilo = 69
boy = 179
vke = round(kilo / ((boy/100)**2), 1)

# --- ANALİZ VE KAYIT ---
if st.button("🚀 SÜRÜŞÜ ANALİZ ET VE GÖNDER"):
    # Erkoz Özel Puanlama Motoru
    std_puan = round(((yas + 20) / 100) * 3 + (vke / 5), 3)
    km_p = round((std_puan / surus_km) * 100, 3)
    rz_p = round((km_p / 10) * (2 if ruzgar_hizi > 15 else 1), 3)
    yk_p = round((yukselti / 1000 * 0.3) + 1, 3)
    final_puan = round(km_p + rz_p + yk_p, 3)

    # 8 SÜTUNLU TAM PAKET (A-H ARASI)
    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": "Mosso Black Edition", 
        "bisKilosu": 10.5,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        # İstek gönderiliyor
        with st.spinner('Veri Excel yolunda, bekleniyor...'):
            response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        
        if response.status_code == 200:
            st.balloons()
            st.success("✅ İŞLEM TAMAM! Veriler milimetrik olarak Excel'e işlendi.")
            
            # GURUR TABLOSU (KISA ÖZET)
            st.markdown(f"""
            <div style="background:#0E1117; border:3px solid #FF4B4B; padding:15px; border-radius:10px; color:white; text-align:center;">
                <h3 style="color:#FF4B4B;">🏆 PERFORMANS SKORU</h3>
                <h1 style="font-size:50px; margin:0;">{final_puan}</h1>
                <p style="color:#888;">{ad_soyad} | {surus_km} KM</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ Sunucu Hatası: {response.status_code}")
            st.info("İpucu: Apps Script'te 'Erişimi olanlar: Herkes' seçili olduğundan emin ol kanka.")
            
    except Exception as e:
        st.error(f"❌ Bağlantı Kesildi: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
