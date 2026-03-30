import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v28.0 - EKSİKSİZ FULL PAKET (SOL PANEL + DEV SERTİFİKA)
st.set_page_config(page_title="Erkoz Analiz v28.0", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TAM PROFİL AYARLARI) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım & Alışkanlık")
bisiklet_markasi = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme Düzeyi (1-3)", [1, 2, 3], index=2, help="1: Zayıf, 2: Orta, 3: Profesyonel")

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Girişi")
sifre = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Yönetici Panelini Aç"):
    if sifre == "erkoz":
        st.session_state.is_admin = True
        st.sidebar.success("Panel Aktif!")
    else:
        st.sidebar.error("Hatalı!")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Grup Terminali")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:50px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">📊 GÜNCEL EXCEL TABLOSUNU AÇ</button></a>', unsafe_allow_html=True)
    st.markdown("---")

st.subheader("🚀 Yeni Sürüş Analizi")
col1, col2 = st.columns(2)

with col1:
    surus_km = st.number_input("Yapılan Mesafe (KM)", value=157.0, step=0.1)
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kalori = st.number_input("Yakılan Toplam Kalori", value=3150)

with col2:
    yukselti = st.number_input("Toplam Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    st.info("Profil verileri sol panelden çekiliyor.")

st.markdown("---")

# --- ANALİZ VE KAYIT MOTORU ---
if st.button("🏁 ANALİZİ TAMAMLA VE EXCEL'E GÖNDER"):
    # --- ORİJİNAL HESAPLAMA SİSTEMİ ---
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    vke_katkisi = round((vke / 100) * 20, 2)
    
    # Standart puan katsayıları
    std_puan = round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_katkisi, 3)
    
    # Sürüş verileriyle harmanlama
    km_puani = round((std_puan / surus_km) * 100, 3)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    
    # FINAL SKOR (13.15 gibi gerçekçi değerler için)
    final_puan = round(km_puani + rz_puan + yk_puan + kalori_bonusu if 'rz_puan' in locals() else km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)
    
    yakilan_yag = round((kalori * 0.8) / 9, 1)

    # Excel Paketi (8 Sütun)
    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": bisiklet_markasi, 
        "bisKilosu": bisiklet_kilosu,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        if response.status_code == 200:
            st.balloons()
            
            # --- DEV BAŞARI BELGESİ (HER ŞEY DAHİL) ---
            st.markdown(f"""
            <div style="background:#0E1117; border:5px double #FF4B4B; padding:25px; border-radius:20px; color:white; font-family:sans-serif;">
                <h1 style="color:#FF4B4B; text-align:center; margin-top:0; letter-spacing:2px;">🏆 ERKOZ PERFORMANS SERTİFİKASI</h1>
                <p style="text-align:center; font-size:22px; margin-bottom:5px;"><b>{ad_soyad}</b></p>
                <p style="text-align:center; color:#888; margin-top:0;">{surus_tarihi} | {bisiklet_markasi}</p>
                
                <hr style="border:0.5px solid #333; margin:20px 0;">
                
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; text-align:center;">
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">Mesafe</small><br><span style="font-size:20px; color:#00D4FF;"><b>{surus_km} KM</b></span>
                    </div>
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">Yükselti</small><br><span style="font-size:20px; color:#00D4FF;"><b>{yukselti} M</b></span>
                    </div>
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">Rüzgar</small><br><span style="font-size:20px; color:#00D4FF;"><b>{ruzgar_hizi} km/h</b></span>
                    </div>
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">Yağ Yakımı</small><br><span style="font-size:20px; color:#32CD32;"><b>{yakilan_yag} gr</b></span>
                    </div>
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">VKE</small><br><span style="font-size:20px; color:#FFD700;"><b>{vke}</b></span>
                    </div>
                    <div style="background:#161B22; padding:15px; border-radius:10px;">
                        <small style="color:#888;">Kalori</small><br><span style="font-size:20px; color:#FF4B4B;"><b>{kalori} kcal</b></span>
                    </div>
                </div>

                <div style="margin-top:25px; background:linear-gradient(145deg, #1f2937, #111827); padding:20px; border-radius:15px; border:2px solid #FF4B4B; text-align:center;">
                    <small style="color:#888; letter-spacing:1px;">GENEL PERFORMANS SKORU</small>
                    <h1 style="color:#FF4B4B; font-size:75px; margin:0; text-shadow: 2px 2px 10px rgba(255,75,75,0.3);">{final_puan}</h1>
                </div>
                
                <p style="text-align:center; margin-top:20px; color:#555; font-style:italic;">Bu analiz Erkoz Yazılım Ar-Ge Laboratuvarlarında doğrulanmıştır.</p>
            </div>
            """, unsafe_allow_html=True)
            st.success("Kanka veriler Excel'e jilet gibi oturdu, sertifikan hazır!")
        else:
            st.error(f"Hata Kodu: {response.status_code}")
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
