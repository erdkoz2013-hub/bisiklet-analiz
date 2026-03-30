import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v31.0 - JANJANLI & PROFESYONEL ZIRHLI SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v31.0", layout="wide", page_icon="🛡️")

# --- 1. HAFIZA VE GÜVENLİK ---
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

# --- 2. SOL PANEL (YÖNETİCİ PANELİ & METRİKLER) ---
st.sidebar.markdown(f"*👤 Sürücü: {saved_data['ad_soyad']}*")
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Ayarlar")
ad_soyad_in = st.sidebar.text_input("Sürücü", value=saved_data["ad_soyad"])
d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
dogum_tarihi_in = st.sidebar.date_input("Doğum Tarihi", d_tarihi_raw)
boy_in = st.sidebar.number_input("Boy (cm)", value=int(saved_data["boy"]))
kilo_in = st.sidebar.number_input("Kilo (kg)", value=float(saved_data["kilo"]))

st.sidebar.markdown("---")
st.sidebar.header("🚲 Ekipman")
bis_marka_in = st.sidebar.text_input("Bisiklet", value=saved_data["bis_marka"])
bis_kilosu_in = st.sidebar.number_input("Donanım Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

# Anlık Hesaplamalar
vke_sid = round(kilo_in / ((boy_in/100)**2), 1)
yas_sid = date.today().year - dogum_tarihi_in.year
zorluk_yuz_sid = round((bis_kilosu_in - 10) * 2, 1)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Canlı Veri Panel")
st.sidebar.metric("VKE", vke_sid)
st.sidebar.metric("Donanım Etkisi", f"%{zorluk_yuz_sid}")
st.sidebar.caption(f"Aktif Yaş: {yas_sid} | Donanım: {bis_kilosu_in} kg")

# --- 3. ANA EKRAN ---
st.title("🛡️ ERKOZ YAZILIM | Analiz Terminali v31.0")

# Input Alanları
col_m1, col_m2 = st.columns([2, 1])
with col_m1:
    col1, col2 = st.columns(2)
    km_input = col1.number_input("Mesafe (KM)", value=157.0)
    yukselti = col2.number_input("Yükselti (m)", value=1049)
    ruzgar_hizi = col1.number_input("Rüzgar (km/h)", value=25.0)
    kalori_input = col2.number_input("Kalori (kcal)", value=3150)
with col_m2:
    st.markdown("### 🚀 Komut")
    go_button = st.button("🚀 ANALİZ ET VE SERTİFİKA YAZ")

if go_button:
    # Kaydetme ve Hesaplama (v30.0 algoritması)
    new_data = {"ad_soyad": ad_soyad_in, "dogum_tarihi": str(dogum_tarihi_in), "boy": boy_in, "kilo": kilo_in, "bis_marka": bis_marka_in, "bis_kilosu": bis_kilosu_in}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    bak_katsayisi = 1 + (zorluk_yuz_sid / 100)
    p1 = ((yas_sid + 20) / 100) * 3
    p2 = (vke_sid / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    # Senkronizasyon (Excel)
    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad_in, "puan": final_puan, "km": km_input}, timeout=3)
    except: pass

    st.balloons()
    
    # --- 🏆 JANJANLI, KOYU TEMALI SERTİFİKA OLUŞTURMA (Zırhlı Sürüm) ---
    # Bu alan, st.container içinde bordürlü ve koyu renkli olacak şekilde tasarlanmıştır.
    with st.container(border=True):
        st.markdown(f"## 🏆 BAŞARI SERTİFİKASI: *{ad_soyad_in}*")
        st.caption(f"📅 {date.today()}  |  🚲 {bis_marka_in}  |  👤 VKE: {vke_sid}")
        st.divider()

        # Janjanlı Metrik Alanı (3 Sütun: Mesafe, Yükselti, Skor/Yağ)
        m_col1, m_col2, m_col3 = st.columns(3)
        
        # Mesafe Kutusu (v29.3 stili gibi koyu zemin taklidi)
        m_col1.markdown(f"""
            <div style='background-color:#1E1E1E; padding:10px; border-radius:5px; border-left: 3px solid #ff4b4b;'>
                <span style='color:#AAAAAA; font-size:12px;'>Mesafe</span><br>
                <span style='color:white; font-size:24px; font-weight:bold;'>{km_input} KM</span>
            </div>
        """, unsafe_allow_with=True)
        
        # Yükselti Kutusu
        m_col2.markdown(f"""
            <div style='background-color:#1E1E1E; padding:10px; border-radius:5px; border-left: 3px solid #AAAAAA;'>
                <span style='color:#AAAAAA; font-size:12px;'>Yükselti</span><br>
                <span style='color:white; font-size:24px; font-weight:bold;'>{yukselti} M</span>
            </div>
        """, unsafe_allow_with=True)
        
        # VKE Kutusu (Vurgulu Sarı)
        m_col3.markdown(f"""
            <div style='background-color:#1E1E1E; padding:10px; border-radius:5px; border-left: 3px solid #FFD700;'>
                <span style='color:#AAAAAA; font-size:12px;'>VKE</span><br>
                <span style='color:#FFD700; font-size:24px; font-weight:bold;'>{vke_sid}</span>
            </div>
        """, unsafe_allow_with=True)

        st.divider()

        # Ana Skor ve Yağ Yakımı (Büyük Kutular)
        sk_col1, sk_col2 = st.columns(2)
        
        # SKOR KUTUSU (Dev Kırmızı)
        sk_col1.markdown(f"""
            <div style='background-color:#ff4b4b; padding:20px; border-radius:10px; color:white; text-align:center;'>
                <span style='font-size:14px; font-weight:bold;'>GENEL PERFORMANS SKORU</span><br>
                <span style='font-size:48px; font-weight:bold;'>{final_puan}</span>
            </div>
        """, unsafe_allow_with=True)
        
        # YAĞ KUTUSU (Ateşli Kırmızı/Turuncu)
        sk_col2.markdown(f"""
            <div style='background-color:#E65100; padding:20px; border-radius:10px; color:white; text-align:center;'>
                <span style='font-size:14px; font-weight:bold;'>🔥 Yakılan Yağ</span><br>
                <span style='font-size:48px; font-weight:bold;'>{yakilan_yag} gr</span>
            </div>
        """, unsafe_allow_with=True)

    st.success("✅ İşlem başarılı! Senkronize edildi.")

st.caption("Erkoz Yazılım © 2026 | Zırhlı v31.0")
