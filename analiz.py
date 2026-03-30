import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v30.0 - KOMPAKT SERTİFİKA SÜRÜMÜ ---
st.set_page_config(page_title="Erkoz Analiz v30.0", layout="wide", page_icon="🚴‍♂️")

# --- 1. HAFIZA SİSTEMİ ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved_data = load_settings()

# --- 2. SOL PANEL ---
st.sidebar.header("👤 Profil & Donanım")
ad_soyad = st.sidebar.text_input("Ad Soyad", value=saved_data["ad_soyad"])
d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", d_tarihi_raw)
boy = st.sidebar.number_input("Boy (cm)", value=int(saved_data["boy"]))
kilo = st.sidebar.number_input("Kilo (kg)", value=float(saved_data["kilo"]))
bis_marka = st.sidebar.text_input("Bisiklet", value=saved_data["bis_marka"])
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

# Hesaplamalar
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = date.today().year - dogum_tarihi.year
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

# --- 3. ANA EKRAN ---
st.title("🚀 Erkoz Analiz Terminali")

st.subheader("🏁 Sürüş Verileri")
c1, c2, c3, c4 = st.columns(4)
with c1: km_input = st.number_input("Mesafe (KM)", value=157.0)
with c2: yukselti = st.number_input("Yükselti (m)", value=1049)
with c3: ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with c4: kalori_input = st.number_input("Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZ ET VE SERTİFİKA OLUŞTUR"):
    # Kaydetme İşlemi
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilosu}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Algoritma
    bak_katsayisi = 1 + (zorluk_yuzdesi / 100)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    # Bulut Aktarımı
    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad, "puan": final_puan, "km": km_input}, timeout=3)
    except: pass

    st.balloons()

    # --- 🏆 YENİ KOMPAKT SERTİFİKA ALANI ---
    with st.container(border=True):
        # Üst Bilgi Satırı
        st.markdown(f"### 🏆 BAŞARI SERTİFİKASI: *{ad_soyad}*")
        st.caption(f"📅 {date.today()}  |  🚲 {bis_marka}  |  👤 VKE: {vke_hesap}")
        
        st.divider()

        # Ana Metrikler (Tek Satırda 4 Sütun)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_input} km")
        m2.metric("Yükselti", f"{yukselti} m")
        m3.metric("Skor", f"{final_puan}")
        m4.metric("Yağ Yakımı", f"{yakilan_yag} g")

    st.success("✅ İşlem başarılı. Ekran görüntüsü alabilirsin!")

st.caption("Erkoz Yazılım © 2026 | v30.0")
