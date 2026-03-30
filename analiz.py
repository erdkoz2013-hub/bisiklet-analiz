import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v48.2 | SESSION SAFE & SPAM PROTECTION ---
st.set_page_config(page_title="Erkoz Analiz v48.2", layout="wide", page_icon="🚴‍♂️")

# --- 1. AYARLAR VE OTURUM YÖNETİMİ ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

# Oturum başlatma (Senin bilgilerin ve KM kilidi hafızası)
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        "ad_soyad": "Erdal Kozal", 
        "dogum_tarihi": "1967-04-03", 
        "boy": 179, 
        "kilo": 69.0, 
        "bis_marka": "Mosso Black Edition", 
        "bis_kilosu": 10.5
    }

# Spam koruması için son gönderilen kilometreyi tutan hafıza
if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# --- 2. SOL PANEL (ERKOZ KONTROL) ---
with st.sidebar:
    st.header("🛡️ Erkoz Kontrol")
    
    ad_soyad = st.text_input("Ad Soyad", value=st.session_state['user_data']["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(st.session_state['user_data']["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(st.session_state['user_data']["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(st.session_state['user_data']["kilo"]))
    
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet Modeli", value=st.session_state['user_data']["bis_marka"])
    bis_kilo = st.number_input("Donanım Ağırlığı (kg)", value=float(st.session_state['user_data']["bis_kilosu"]))

    # Oturumu güncelle
    st.session_state['user_data'].update({
        "ad_soyad": ad_soyad, "dogum_tarihi": str(d_tarihi), "boy": boy, "kilo": kilo,
        "bis_marka": bis_marka, "bis_kilosu": bis_kilo
    })

    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    st.sidebar.metric("Anlık VKE", vke)
    st.sidebar.metric("Zorluk Katsayısı", f"%{zorluk}")

# --- 3. ANA EKRAN ---
st.title("🚀 Erkoz Yazılım | Performans Analiz")

col1, col2 = st.columns(2)
with col1:
    km_in = st.number_input("Sürüş Mesafesi (KM)", value=157.0)
    ruz_in = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
with col2:
    yuk_in = st.number_input("Toplam Yükselti (m)", value=1049)
    kal_in = st.number_input("Yakılan Kalori (kcal)", value=3150)

# --- 4. ANALİZ VE AKILLI KİLİT ---
if st.button("🚀 ANALİZİ TAMAMLA VE EXCEL'E AKTAR"):
    
    # 🛑 SPAM KONTROLÜ: Aynı kilometre ise durdur!
    if km_in == st.session_state['last_km']:
        st.error(f"⚠️ Hop! {km_in} KM verisi zaten az önce gönderildi. Kayıt mükerrer olmasın diye engellendi kanka.")
    else:
        # Hesaplamalar
        yas = date.today().year - d_tarihi.year
        bak = 1 + (zorluk / 100)
        final_puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
        yag_gr = round((kal_in * 0.8) / 9, 1)

        payload = {
            "adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilo,
            "surusTarihi": str(date.today()), "surusKM": km_in, "ruzgarHizi": ruz_in,
            "yukselti": yuk_in, "puan": final_puan
        }
        
        try:
            requests.post(SCRIPT_URL, json=payload, timeout=7)
            st.success(f"✅ Excel Senkronizasyonu Başarılı! (Puan: {final_puan})")
            # ✅ BAŞARILI GÖNDERİM SONRASI KİLİDİ GÜNCELLE
            st.session_state['last_km'] = km_in
        except Exception as e:
            st.warning("⚠️ Excel bağlantısı kurulamadı.")

        # --- 🏆 SERTİFİKA ---
        st.divider()
        with st.container(border=True):
            st.header(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
            st.write(f"📅 *Tarih:* {date.today()} | 🚲 *Ekipman:* {bis_marka} | 👤 *VKE:* {vke}")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mesafe", f"{km_in} KM")
            m2.metric("Yükselti", f"{yuk_in} M")
            m3.metric("Skor", final_puan)
            m4.metric("Yağ Yakımı", f"{yag_gr} gr")
            st.divider()
            res1, res2 = st.columns(2)
            res1.error(f"🎯 *GENEL PERFORMANS SKORU*: {final_puan}")
            res2.warning(f"🔥 *TOPLAM YAKILAN YAĞ*: {yag_gr} gr")

st.caption("Erkoz Yazılım © 2026 | v48.2 - Multi-User & Anti-Spam Master")
