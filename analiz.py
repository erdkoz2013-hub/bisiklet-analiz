import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v29.0 - BALONLAR KALDIRILDI, SERTİFİKA STABİLİZE EDİLDİ
st.set_page_config(page_title="Erkoz Analiz v29.0", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (PROFİL & CANLI DONANIM ANALİZİ) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım Analizi")
bis_marka = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5, step=0.1)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme", [1, 2, 3], index=2)

# Canlı Hesaplamalar
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = 2026 - dogum_tarihi.year
# 10kg referanslı zorluk katsayısı
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)
bak_katsayisi = 1 + (zorluk_yuzdesi / 100)

st.sidebar.markdown("---")
st.sidebar.metric("Anlık VKE", vke_hesap)
st.sidebar.metric("Donanım Etkisi", f"%{zorluk_yuzdesi}", delta=zorluk_yuzdesi, delta_color="inverse")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Terminal")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">📊 EXCEL TABLOSUNU AÇ</button></a>', unsafe_allow_html=True)
    st.markdown("---")

st.subheader("🏁 Sürüş Verileri")
col1, col2 = st.columns(2)
with col1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with col2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())

# --- ANALİZ MOTORU ---
if st.button("🚀 ANALİZİ TAMAMLA"):
    # 1. Standart Puan (Excel Senkronize)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    p3 = (haftalik_km / 100) * 1.5
    p4 = (beslenme / 1) * 1.3
    
    # Bisiklet ağırlığı standart puanı etkiler
    standart_puan = (p1 + p2 + p3 + p4) * bak_katsayisi
    
    # 2. Sürüş Puanları
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_p = (km_p * kademe) / 10
    yukselti_p = (yukselti / 1000 * 0.3) + 1
    
    final_puan = round(km_p + ruzgar_p + yukselti_p, 3)

    # Renk ve İşaret Ayarı
    fark_isareti = "+" if zorluk_yuzdesi >= 0 else ""
    katsayi_rengi = "#FF4B4B" if zorluk_yuzdesi >= 0 else "#32CD32"

    # VERİ GÖNDERİMİ
    payload = {"adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilosu, "surusTarihi": str(surus_tarihi), "surusKM": km_input, "ruzgarHizi": ruzgar_hizi, "yukselti": yukselti, "puan": final_puan}
    
    try:
        # Balonlar sildiğimiz için direkt sertifikaya geçiyoruz
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        
        # --- GÜVENLİ SERTİFİKA TASARIMI ---
        st.markdown(f"""
        <div style="background-color:#0E1117; border:5px solid #FF4B4B; padding:25px; border-radius:20px; color:white; text-align:center; font-family:sans-serif;">
            <h1 style="color:#FF4B4B; margin:0;">🏆 BAŞARI SERTİFİKASI</h1>
            <h2 style="margin:10px 0;">{ad_soyad}</h2>
            <p style="color:#888;">{surus_tarihi} | {bis_marka}</p>
            <hr style="border:0.5px solid #333; margin:20px 0;">
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-bottom:20px;">
                <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>Mesafe</small><br><b>{km_input} KM</b></div>
                <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>Yükselti</small><br><b>{yukselti} M</b></div>
                <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>VKE</small><br><b style="color:#FFD700;">{vke_hesap}</b></div>
            </div>
            <div style="margin-bottom:15px; font-size:14px; background-color:#161B22; padding:10px; border-radius:10px;">
                ⚙️ Donanım: {bis_kilosu} kg | Zorluk Etkisi: <b style="color:{katsayi_rengi};">{fark_isareti}%{zorluk_yuzdesi}</b>
            </div>
            <div style="background:linear-gradient(145deg, #FF4B4B, #8B0000); padding:20px; border-radius:15px;">
                <p style="margin:0; font-size:14px; opacity:0.8;">GENEL PERFORMANS SKORU</p>
                <h1 style="font-size:65px; margin:0; font-weight:bold;">{final_puan}</h1>
            </div>
            <p style="margin-top:15px; font-size:13px; color:#32CD32;">✅ Donanım ve Excel Analizi Senkronize Edildi</p>
        </div>
        """, unsafe_allow_html=True)
        st.success("✅ İşlem Başarılı. Kod kirliliği engellendi!")
    except:
        st.error("Bağlantı kurulamadı!")

# Yönetici Şifre
if not st.session_state.is_admin:
    with st.sidebar.expander("🔑 Yönetici Girişi"):
        if st.text_input("Şifre", type="password") == "erkoz":
            st.session_state.is_admin = True
            st.rerun()

st.caption("Erkoz Yazılım © 2026")
