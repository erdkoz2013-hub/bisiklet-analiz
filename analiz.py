import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v26.3 - ÇELİK HAFIZA & YÖNETİCİ PANELİ (KESİN ÇÖZÜM)
st.set_page_config(page_title="Erkoz Analiz v26.3", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
ADMIN_PASSWORD = "erkoz" 
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

# --- HAFIZA KONTROLÜ (Telefonda Sayfa Yenilenince Unutmasın Diye) ---
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- YÖNETİCİ GİRİŞİ ---
st.sidebar.header("🔑 Yönetici Alanı")
sifre_denemesi = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Girişi Onayla"):
    if sifre_denemesi == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("Hoş geldin Patron!")
    else:
        st.sidebar.error("Hatalı Şifre!")

if st.session_state.is_admin:
    st.sidebar.info("✅ Yönetici Modu Aktif")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.is_admin = False
        st.rerun()

# --- ANA EKRAN ---
if st.session_state.is_admin:
    st.success("🏁 *YÖNETİCİ MODU AKTİF:* Tüm yetkiler Erdal Kozal'da. Listeniz sayfanın en altında hazır!")

st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Sistemi")
st.markdown("---")

# --- KAYIT FORMU ---
st.sidebar.header("👤 Sürücü Bilgileri")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)
bisiklet = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")

col1, col2 = st.columns(2)
with col1:
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=100.0)
    kalori = st.number_input("Yakılan Kalori", value=2500)
with col2:
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    yukselti = st.number_input("Yükselti (m)", value=1049)

# --- VERİ İŞLEME ---
if st.button("🚀 SÜRÜŞÜ ERKOZ SİSTEMİNE KAYDET"):
    # (Hesaplamalar burada yapılıyor...)
    vke = round(kilo / ((boy/100)**2), 1)
    vke_katkisi = round((vke / 100) * 20, 2)
    km_puani = round((10.0 / surus_km) * 100, 3)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    yakilan_yag = round((kalori * 0.8) / 9, 1)
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu + vke_katkisi, 3)

    payload = {
        "adSoyad": ad_soyad, "s_km": surus_km, "puan": final_puan, "yag": yakilan_yag
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        st.success(f"Tebrikler {ad_soyad}! Verilerin Erdal Kozal'ın ana tablosuna işlendi.")
        cert_html = f"<div style='border:4px solid #FF4B4B; padding:15px; border-radius:10px; background:#0E1117; color:white; text-align:center;'><h3>🏆 PUAN: {final_puan}</h3><p>{yakilan_yag}g Yağ Yakımı</p></div>"
        st.components.v1.html(cert_html, height=200)
    except:
        st.error("Bağlantı hatası.")

# --- İŞTE O GİZLİ PANEL ---
if st.session_state.is_admin:
    st.markdown("---")
    st.header("🏁 Erkoz Yönetici Paneli")
    st.warning("Kanka, tüm grubun aylık listesi aşağıda seni bekliyor!")
    
    # Dev gibi bir buton ve link
    st.markdown(f"""
        <a href="{SHEETS_LINK}" target="_blank">
            <button style="width:100%; height:80px; background-color:#FF4B4B; color:white; border:none; border-radius:15px; font-size:20px; font-weight:bold; cursor:pointer;">
                📊 TÜM GRUP LİSTESİNİ (GOOGLE SHEETS) AÇ
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    st.info("💡 Üstteki kırmızı butona bastığında Google Sheets tablan yeni bir sekmede açılacaktır.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Performans Analiz Merkezi")
