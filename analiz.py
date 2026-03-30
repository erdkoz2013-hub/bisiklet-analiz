import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v26.0 - GRUP KAYIT & YÖNETİCİ PANELİ (TAM KOD)
st.set_page_config(page_title="Erkoz Analiz v26.0", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR VE ŞİFRE ---
ADMIN_PASSWORD = "erkoz"  # Kanka burayı istersen değiştir
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# Görsel Stil Ayarları
st.markdown("""
    <style>
        .report-label { color: #A8B2BD !important; font-size: 14px !important; }
        .report-value { color: #FFFFFF !important; font-size: 18px !important; font-weight: bold !important; }
        .score-box { background-color: #1F2937 !important; padding: 15px !important; border-radius: 10px !important; border: 3px solid #FF4B4B !important; text-align: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- MATEMATİKSEL MOTOR ---
def ruzgar_kademesi_bul(hiz):
    if hiz <= 15: return 1
    elif hiz <= 31: return 2
    else: return 3

def hesapla_standart_puan(yas, haftalik_km, beslenme, vke_puani):
    return round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_puani, 3)

# --- SOL PANEL (SÜRÜCÜ PROFİLİ & GİRİŞ) ---
st.sidebar.header("👤 Sürücü Kayıt")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)
bisiklet = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Alanı")
admin_input = st.sidebar.text_input("Şifre", type="password", help="Sadece Erdal Kozal içindir.")
login_button = st.sidebar.button("Yönetici Girişini Onayla")

# --- ANA EKRAN (SÜRÜŞ VERİLERİ) ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Sistemi")
st.info("Arkadaşların bu formu doldurup 'KAYDET'e bastığında veriler senin tablona düşer.")

col1, col2 = st.columns(2)
with col1:
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=100.0)
    kalori = st.number_input("Yakılan Kalori (kcal)", value=2500)

with col2:
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    if ruzgar_hizi <= 15: st.info("🌬️ 1. Kademe (Hafif)")
    elif ruzgar_hizi <= 31: st.warning("🌪️ 2. Kademe (Orta)")
    else: st.error("🌀 3. Kademe (Sert!)")
    
    yukselti = st.number_input("Yükselti (m)", value=1049)

# --- HESAPLAMALAR VE KAYIT ---
if st.button("🚀 SÜRÜŞÜ KAYDET VE ANALİZ ET"):
    # Teknik Hesaplamalar
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    vke_katkisi = round((vke / 100) * 20, 2)
    std_puan = hesapla_standart_puan(yas, 200, 3, vke_katkisi)
    
    km_puani = round((std_puan / surus_km) * 100, 3)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    yakilan_yag = round((kalori * 0.8) / 9, 1)
    
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)

    # Google Sheets Payload
    payload = {
        "adSoyad": ad_soyad, "boy": boy, "kilo": kilo, "bisiklet": bisiklet,
        "s_tarih": str(surus_tarihi), "s_km": surus_km, "ruzgar": ruzgar_hizi,
        "yukselti": yukselti, "puan": final_puan, "kalori": kalori, "yag": yakilan_yag
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # Sertifika Tasarımı (HTML)
        cert_html = f"""
        <div style="background-color: #0E1117; border: 5px double #FF4B4B; padding: 20px; border-radius: 15px; font-family: sans-serif; color: white;">
            <h2 style="color: #FF4B4B; text-align: center; margin-top: 0;">🏆 ERKOZ PERFORMANS ANALİZİ</h2>
            <p style="text-align: center; color: #888;">Tarih: {surus_tarihi}</p>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <span>Sürücü: <b>{ad_soyad}</b></span>
                <span>Bisiklet: <b>{bisiklet}</b></span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background:#161B22; padding:10px; border-radius:8px;">KM Puanı: {km_puani}</div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">Rüzgar: +{ruzgar_katkisi}</div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">Tırmanış: +{yukselti_puani}</div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">Yağ Yakımı: {yakilan_yag}g</div>
            </div>
            <div style="margin-top: 15px; background: #1F2937; padding: 15px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                <h1 style="color: #FF4B4B; font-size: 50px; margin: 0;">{final_puan}</h1>
                <small>GENEL SKOR</small>
            </div>
            <div style="margin-top: 15px; text-align: right; border-top: 1px solid #333; padding-top: 5px;">
                <small style="color: #555;">Analiz Onay</small><br>
                <span style="font-family: cursive; font-size: 18px;">Erdal Kozal</span>
            </div>
        </div>
        """
        st.components.v1.html(cert_html, height=500)
        st.success(f"{ad_soyad}, verilerin başarıyla Erkoz veritabanına kaydedildi!")
    except:
        st.error("Bağlantı hatası! Lütfen internetinizi kontrol edin.")

# --- YÖNETİCİ PANELİ (GİZLİ) ---
if admin_input == ADMIN_PASSWORD or login_button:
    if admin_input == ADMIN_PASSWORD:
        st.markdown("---")
        st.header("🏁 Erkoz Yönetici Paneli")
        st.success("Hoş geldin Erdal Kozal! Grup yönetim yetkileri aktif.")
        
        # Ay Sonu Raporu Butonu
        if st.button("📊 AY SONU TOPLU LİSTEYİ AÇ"):
            st.info("Kanka, tüm arkadaşların verileri şu an Google Sheets tablanda toplanmış durumda.")
            st.write("👉 [BURAYA TIKLAYARAK TABLOYU GÖRÜNTÜLE](https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M)")
    elif login_button:
        st.sidebar.error("Şifre Yanlış Kanka!")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Performans Analiz Merkezi")
