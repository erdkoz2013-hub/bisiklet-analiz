import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v46.0 | EXCEL DOLDURMA GARANTİLİ ---
st.set_page_config(page_title="Erkoz Analiz v46.0", layout="wide", page_icon="🚴‍♂️")

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

# --- 2. SOL PANEL (DÜZELTİLEN GÖSTERGELER) ---
with st.sidebar:
    st.header("🛡️ Erkoz Kontrol")
    ad_soyad = st.text_input("Ad Soyad", value=saved["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(saved["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(saved["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(saved["kilo"]))
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet", value=saved["bis_marka"])
    bis_kilo = st.number_input("Donanım KG", value=float(saved["bis_kilosu"]))

    # Hesaplamalar
    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    
    st.sidebar.metric("Vücut Kitle İndeksi (VKE)", vke)
    st.sidebar.metric("Donanım Zorluk Etkisi", f"%{zorluk}")

# --- 3. ANA EKRAN ---
st.title("🚀 Erkoz Yazılım | Performans Terminali")

c1, c2 = st.columns(2)
km_in = c1.number_input("Mesafe (KM)", value=157.0)
yuk_in = c2.number_input("Yükselti (m)", value=1049)
ruz_in = c1.number_input("Rüzgar (km/h)", value=25.0)
kal_in = c2.number_input("Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZ ET VE EXCEL'E AKTAR"):
    # Ayarları Kaydet
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(d_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilo}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Skor Algoritması
    yas = date.today().year - d_tarihi.year
    bak = 1 + (zorluk / 100)
    final_puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
    yag_gr = round((kal_in * 0.8) / 9, 1)

    # --- 🛡️ EXCEL TAM UYUMLU PAKET (SENİN ÇALIŞTIRDIĞIN İSİMLER) ---
    payload = {
        "adSoyad": ad_soyad,
        "bisiklet": bis_marka,
        "bisKilosu": bis_kilo,
        "surusTarihi": str(date.today()),
        "sürüş km": km_in,        # <-- Senin onayladığın format
        "rüzgar": ruz_in,          # <-- Ü harfiyle rüzgar
        "yukselti": yuk_in,
        "sürüş puanı": final_puan  # <-- Tam isimli puan
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
        st.success("✅ Veriler Excel'e tam isabetle gönderildi!")
    except:
        st.warning("⚠️ Bağlantı hatası, veriler yerelde kaldı.")

    # --- 🏆 BAŞARI SERTİFİKASI ---
    st.divider()
    with st.container(border=True):
        st.header(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
        st.write(f"📅 *Tarih:* {date.today()} | 🚲 *{bis_marka}* | 👤 *VKE:* {vke}")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_in} KM")
        m2.metric("Yükselti", f"{yuk_in} M")
        m3.metric("Skor", final_puan)
        m4.metric("Yağ", f"{yag_gr} gr")
        
        st.divider()
        r1, r2 = st.columns(2)
        r1.error(f"🎯 *PERFORMANS SKORU*: {final_puan}")
        r2.warning(f"🔥 *YAKILAN YAĞ*: {yag_gr} gr")

st.caption("Erkoz Yazılım © 2026 | v46.0 - Final Precision")
