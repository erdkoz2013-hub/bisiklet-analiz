import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v39.0 | GERÇEK EFSANE SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v39.0", layout="wide", page_icon="🛡️")

# --- 1. AYARLAR ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved = load_settings()

# --- 2. SOL PANEL (ADMİN PANELİ GERİ GELDİ) ---
with st.sidebar:
    st.header("🛡️ Kontrol Paneli")
    ad_soyad = st.text_input("Sürücü", value=saved["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(saved["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(saved["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(saved["kilo"]))
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet", value=saved["bis_marka"])
    bis_kilo = st.number_input("Donanım KG", value=float(saved["bis_kilosu"]))

    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    st.sidebar.metric("VKE", vke)
    st.sidebar.metric("Zorluk Etkisi", f"%{zorluk}")

# --- 3. ANA TERMİNAL ---
st.title("🚀 Erkoz Yazılım | Performans Terminali")

c1, c2 = st.columns(2)
km_in = c1.number_input("Sürüş Mesafesi (KM)", value=157.0)
yuk_in = c2.number_input("Toplam Yükselti (m)", value=1049)
ruz_in = c1.number_input("Rüzgar Hızı (km/h)", value=25.0)
kal_in = c2.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ ÇALIŞTIR VE GÜVENLİ AKTAR"):
    # Ayarları Kaydet
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(d_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilo}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Hesaplama Algoritması
    yas = date.today().year - d_tarihi.year
    bak = 1 + (zorluk / 100)
    skor = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
    yag = round((kal_in * 0.8) / 9, 1)

    # --- 🛡️ EXCEL SENKRONİZASYON (ESKİ ÇALIŞAN İSİMLERE DÖNÜLDÜ) ---
    # Excel'e gitmeyen verileri o eski, çalışan değişken isimleriyle paketledim.
    payload = {
        "adSoyad": ad_soyad,
        "puan": skor,
        "km": km_in,
        "yukselti": yuk_in,
        "ruzgar": ruz_in,
        "kalori": kal_in,
        "bisiklet": bis_marka,
        "tarih": str(date.today())
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
        st.success("✅ Erkoz Veri Tankı Senkronize Edildi!")
    except:
        st.warning("⚠️ Bulut senkronizasyonu başarısız, yerel kayıt tamam.")

    # --- 🏆 JANJANLI SERTİFİKA (v29.3 TASARIMI) ---
    st.divider()
    with st.container(border=True):
        st.header(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
        st.write(f"📅 *Tarih:* {date.today()} | 🚲 *Ekipman:* {bis_marka} | 👤 *VKE:* {vke}")
        
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_in} KM")
        m2.metric("Yükselti", f"{yuk_in} M")
        m3.metric("Skor", skor)
        m4.metric("Yağ Yakımı", f"{yag} gr")
        
        st.divider()
        # v29.3'teki o büyük kırmızı/turuncu alanları geri getirdik
        res1, res2 = st.columns(2)
        res1.error(f"🎯 *GENEL PERFORMANS SKORU*: {skor}")
        res2.warning(f"🔥 *TOPLAM YAKILAN YAĞ*: {yag} gr")

st.caption("Erkoz Yazılım © 2026 | v39.0 - Efsane Geri Döndü")
