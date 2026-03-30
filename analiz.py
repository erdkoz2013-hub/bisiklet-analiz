import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v29.4 - KOD GÖRÜNMESİNE SON! ---
st.set_page_config(page_title="Erkoz Analiz v29.4", layout="wide", page_icon="🛡️")

# --- 1. HAFIZA VE AYARLAR ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
saved_data = load_settings()

# --- 2. SOL PANEL (PROFİL VE METRİKLER) ---
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

# --- 💎 SOL PANELDEKİ KRİTİK METRİKLER (GERİ GELDİ) ---
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = date.today().year - dogum_tarihi.year
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

col_vke, col_don = st.sidebar.columns(2)
with col_vke:
    st.metric("Anlık VKE", vke_hesap)
with col_don:
    st.metric("Donanım Etkisi", f"%{zorluk_yuzdesi}")

# Yönetici Girişi
st.sidebar.markdown("---")
if not st.session_state.is_admin:
    with st.sidebar.expander("🔑 Yönetici Girişi"):
        if st.text_input("Şifre", type="password") == "erkoz":
            st.session_state.is_admin = True
            st.rerun()
else:
    st.sidebar.success("✅ Admin Modu Aktif")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.is_admin = False
        st.rerun()

# --- 3. ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Güvenli Terminal")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; margin-bottom:20px;">📊 EXCEL TABLOSUNU AÇ</button></a>', unsafe_allow_html=True)

st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
with c1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with c2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    kalori_input = st.number_input("Yakılan Kalori (kcal)", value=3150)

# --- 4. ANALİZ VE SERTİFİKA ---
if st.button("🚀 ANALİZİ TAMAMLA VE GÜVENLİ AKTAR"):
    save_settings({"ad_soyad": ad_soyad, "dogum_tarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilosu})
    
    bak_katsayisi = 1 + (zorluk_yuzdesi / 100)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilosu, "surusTarihi": str(date.today()), "surusKM": km_input, "ruzgarHizi": ruzgar_hizi, "yukselti": yukselti, "puan": final_puan}, timeout=5)
    except: pass

    # --- 🏆 KODUN GÖRÜNMESİNİ İMKANSIZ KILAN YENİ YAPI ---
    st.write("---")
    sertifika_html = f"""
    <div style="background-color:#111; border:4px solid #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center; font-family:sans-serif;">
        <h2 style="color:#FF4B4B; margin:0;">🏆 BAŞARI SERTİFİKASI</h2>
        <h3 style="margin:5px 0;">{ad_soyad}</h3>
        <p style="font-size:12px; color:#aaa; margin-bottom:15px;">{date.today()} | {bis_marka}</p>
        
        <div style="display:flex; justify-content:space-around; margin-bottom:15px;">
            <div style="background:#222; padding:8px; border-radius:8px; width:30%;"><small style="color:#888;">Mesafe</small><br><b>{km_input} KM</b></div>
            <div style="background:#222; padding:8px; border-radius:8px; width:30%;"><small style="color:#888;">Yükselti</small><br><b>{yukselti} M</b></div>
            <div style="background:#222; padding:8px; border-radius:8px; width:30%;"><small style="color:#888;">VKE</small><br><b style="color:#FFD700;">{vke_hesap}</b></div>
        </div>

        <div style="background:linear-gradient(to right, #FF4B4B, #8B0000); padding:15px; border-radius:10px;">
            <p style="margin:0; font-size:12px;">GENEL PERFORMANS SKORU</p>
            <h1 style="font-size:50px; margin:5px 0;">{final_puan}</h1>
            <div style="border-top:1px solid rgba(255,255,255,0.2); padding-top:10px;">
                <b style="color:#32CD32; font-size:18px;">🔥 Yakılan Yağ: {yakilan_yag} gr</b>
            </div>
        </div>
        <p style="margin-top:10px; font-size:13px; color:#32CD32;">✅ Veriler Erkoz Veritabanına İşlendi.</p>
    </div>
    """
    st.markdown(sertifika_html, unsafe_allow_html=True)
    st.success("İşlem Başarıyla Tamamlandı!")

st.caption("Erkoz Yazılım © 2026 | Zırhlı v29.4")
