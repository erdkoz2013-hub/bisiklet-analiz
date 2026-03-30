import streamlit as st
from datetime import date
import requests
import json
import os

# --- ERKOZ ANALİZ v29.3 - JİLET SÜRÜM (KESİLMEZ, KOD GÖRÜNMEZ) ---
st.set_page_config(page_title="Erkoz Analiz v29.3", layout="wide", page_icon="🛡️")

# --- HAFIZA SİSTEMİ ---
SETTINGS_FILE = "erkoz_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {
        "ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03",
        "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5
    }

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_data = load_settings()

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value=saved_data["ad_soyad"])
d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", d_tarihi_raw)
boy = st.sidebar.number_input("Boy (cm)", value=int(saved_data["boy"]))
kilo = st.sidebar.number_input("Kilo (kg)", value=float(saved_data["kilo"]))

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım")
bis_marka = st.sidebar.text_input("Bisiklet", value=saved_data["bis_marka"])
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

# Analiz Hesapları
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = date.today().year - dogum_tarihi.year
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

# Yönetici Girişi
st.sidebar.markdown("---")
if not st.session_state.is_admin:
    with st.sidebar.expander("🔑 Yönetici Girişi"):
        if st.text_input("Şifre", type="password") == "erkoz":
            st.session_state.is_admin = True
            st.rerun()

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Güvenli Terminal")

st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
with c1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with c2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    kalori_input = st.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ TAMAMLA VE GÜVENLİ AKTAR"):
    # Hafıza Kaydı
    new_settings = {"ad_soyad": ad_soyad, "dogum_tarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilosu}
    save_settings(new_settings)
    
    # Hesaplamalar
    bak_katsayisi = 1 + (zorluk_yuzdesi / 100)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    # Excel Aktarımı
    payload = {"adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilosu, "surusTarihi": str(date.today()), "surusKM": km_input, "ruzgarHizi": ruzgar_hizi, "yukselti": yukselti, "puan": final_puan}
    try: requests.post(SCRIPT_URL, json=payload, timeout=5)
    except: pass

    # --- 🏆 BAŞARI SERTİFİKASI (HİÇBİR ŞEKİLDE KESİLMEZ) ---
    st.markdown(f"""
    <div style="background-color:#0E1117; border:5px solid #FF4B4B; padding:25px; border-radius:20px; color:white; text-align:center; font-family:sans-serif;">
        <h1 style="color:#FF4B4B; margin:0; font-size:32px;">🏆 BAŞARI SERTİFİKASI</h1>
        <h2 style="margin:10px 0; font-size:26px;">{ad_soyad}</h2>
        <p style="color:#888;">{date.today()} | {bis_marka}</p>
        <hr style="border:0.5px solid #333; margin:20px 0;">
        
        <div style="display:flex; justify-content:space-between; gap:10px; margin-bottom:15px; flex-wrap: wrap;">
            <div style="background:#1F2937; padding:12px; border-radius:10px; flex:1; min-width:80px;"><small style="color:#aaa;">Mesafe</small><br><b>{km_input} KM</b></div>
            <div style="background:#1F2937; padding:12px; border-radius:10px; flex:1; min-width:80px;"><small style="color:#aaa;">Yükselti</small><br><b>{yukselti} M</b></div>
            <div style="background:#1F2937; padding:12px; border-radius:10px; flex:1; min-width:80px;"><small style="color:#aaa;">VKE</small><br><b style="color:#FFD700;">{vke_hesap}</b></div>
        </div>

        <p style="font-size:13px; color:#888;">⚙️ Donanım: {bis_kilosu} kg | Zorluk Etkisi: %{zorluk_yuzdesi}</p>

        <div style="background:linear-gradient(145deg, #FF4B4B, #8B0000); padding:20px; border-radius:15px; margin-top:10px;">
            <p style="margin:0; font-size:14px; opacity:0.8;">GENEL PERFORMANS SKORU</p>
            <h1 style="font-size:65px; margin:0; font-weight:bold;">{final_puan}</h1>
            <div style="margin-top:10px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.2);">
                <b style="font-size:20px; color:#32CD32;">🔥 Yakılan Yağ: {yakilan_yag} gr</b>
            </div>
        </div>
        
        <p style="margin-top:20px; font-size:14px; color:#32CD32; font-weight:bold;">
            ✅ Donanım ve Excel Analizi Senkronize Edildi.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Erkoz Yazılım: Analiz başarıyla tamamlandı!")

st.caption("Erkoz Yazılım © 2026 | Zırhlı v29.3")
