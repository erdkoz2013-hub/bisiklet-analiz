import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v37.0 - FULL DATA SYNC & JANJANLI SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v37.0", layout="wide", page_icon="🛡️")

# --- 1. AYARLAR & URL ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved = load_settings()

# --- 2. SOL PANEL (KONTROL PANELİ) ---
with st.sidebar:
    st.header("👤 Sürücü & Donanım")
    ad_soyad = st.text_input("Ad Soyad", value=saved["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(saved["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(saved["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(saved["kilo"]))
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet Modeli", value=saved["bis_marka"])
    bis_kilo = st.number_input("Bisiklet Ağırlığı (kg)", value=float(saved["bis_kilosu"]))

    # Anlık Metrikler
    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    yas = date.today().year - d_tarihi.year
    st.sidebar.metric("Anlık VKE", vke)
    st.sidebar.metric("Zorluk Katsayısı", f"%{zorluk}")

# --- 3. ANA TERMİNAL ---
st.title("🚀 Erkoz Yazılım | Performans Terminali")

st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
km_in = c1.number_input("Mesafe (KM)", value=157.0)
ruz_in = c1.number_input("Rüzgar Hızı (km/h)", value=25.0)
yuk_in = c2.number_input("Yükselti Kazanımı (m)", value=1049)
kal_in = c2.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZ ET VE EXCEL'E FULL AKTAR"):
    # 1. Yerel Kayıt
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(d_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilo}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # 2. Algoritma Hesaplama
    bak = 1 + (zorluk / 100)
    skor = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
    yag = round((kal_in * 0.8) / 9, 1)

    # 3. EXCEL FULL SENKRONİZASYON (İstediğin Tüm Veriler Buraya Eklendi)
    payload = {
        "tarih": str(date.today()),
        "adSoyad": ad_soyad,
        "bisiklet": bis_marka,
        "bisikletKilosu": bis_kilo,
        "km": km_in,
        "yukselti": yuk_in,
        "ruzgar": ruz_in,
        "kalori": kal_in,
        "vke": vke,
        "puan": skor,
        "yagYakimi": yag
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
        st.success("✅ Tüm veriler Excel tablosuna başarıyla işlendi!")
    except:
        st.warning("⚠️ Excel bağlantısında bir sorun oluştu ama sertifika hazır!")

    # 4. 🏆 JANJANLI SERTİFİKA ALANI
    st.divider()
    with st.container(border=True):
        st.subheader(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
        st.write(f"📅 Tarih: {date.today()} | 🚲 {bis_marka} | 👤 VKE: {vke}")
        st.divider()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_in} km")
        m2.metric("Yükselti", f"{yuk_in} m")
        m3.metric("Skor", skor)
        m4.metric("Yağ", f"{yag} g")
        
        st.divider()
        res_c1, res_c2 = st.columns(2)
        res_c1.error(f"🎯 PERFORMANS SKORU: {skor}")
        res_c2.warning(f"🔥 YAKILAN YAĞ: {yag} gr")

st.caption("Erkoz Yazılım © 2026 | v37.0 - Full Sync Armor")
