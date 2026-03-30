import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v26.5 - TAM İSABET GÜNCELLEMESİ (EXCEL TAMİRİ & MOBİL UYUM)
st.set_page_config(page_title="Erkoz Analiz v26.5", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
ADMIN_PASSWORD = "erkoz" 
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TÜM TEKNİK DETAYLAR) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)
st.sidebar.markdown("---")
st.sidebar.header("🚲 Bisiklet & Performans")
# Excel'deki başlıkla eşleşmesi için küçük harf: bisikleti
bisiklet_modeli = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme Düzeni (1-3)", [1, 2, 3], index=2)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Alanı")
sifre_denemesi = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Girişi Onayla"):
    if sifre_denemesi == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("Hoş geldin Patron!")
    else:
        st.sidebar.error("Hatalı Şifre!")

# --- ANA EKRAN ---
if st.session_state.is_admin:
    st.success("🏁 YÖNETİCİ MODU AKTİF - Verileriniz pırıl pırıl işleniyor kanka.")

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Performans Analizi")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Verileri")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=157.0)
    # Excel'deki başlıkla eşleşmesi için: yakilanKalori
    kalori = st.number_input("Yakılan Toplam Kalori (kcal)", value=3150)

with col2:
    st.subheader("🌤️ Dış Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    
    yukselti = st.number_input("Tırmanış / Yükselti (m)", value=1049)

# --- ANALİZ VE KAYIT ---
if st.button("🚀 ANALİZİ TAMAMLA VE KAYDET"):
    # Matematiksel Motor
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    vke_katkisi = round((vke / 100) * 20, 2)
    
    # Standart Puan Hesaplama (Ar-Ge Formülü)
    std_puan = round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_katkisi, 3)
    
    km_puani = round((std_puan / surus_km) * 100, 3)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    # Excel'deki başlıkla eşleşmesi için: yakilanYag
    yakilan_yag = round((kalori * 0.8) / 9, 1)
    
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)

    # --- EXCEL TAMİRİ (SÜTUN SIRALAMASI VE TAM VERİ) ---
    # Bu isimler Excel tablonun Kod.gs'deki değişken isimleriyle tam eşleşmelidir.
    payload = {
        "adSoyad": ad_soyad, 
        "dogumTarihi": str(dogum_tarihi),
        "boy": boy, 
        "kilo": kilo, 
        "bisikleti": bisiklet_modeli, # Eşleşme sağlandı
        "bisKilosu": bisiklet_kilosu, # Eşleşme sağlandı
        "haftalikKM": haftalik_km,
        "beslenme": beslenme,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan, 
        "yakilanKalori": kalori, # Eşleşme sağlandı
        "yakilanYag": yakilan_yag # Eşleşme sağlandı
    }
    
    try:
        # Google Sheets'e veri gönderme
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # --- O MEŞHUR DEV BAŞARI BELGESİ (HTML) - MOBİL UYUM ---
        cert_html = f"""
        <div style="background-color: #0E1117; border: 5px double #FF4B4B; padding: 15px; border-radius: 12px; font-family: sans-serif; color: white; max-width: 600px; margin: auto;">
            <h2 style="color: #FF4B4B; text-align: center; margin-top: 0; font-size: 22px;">🏆 ERKOZ PERFORMANS ANALİZİ</h2>
            <p style="text-align: center; color: #888; font-size: 12px; margin: 5px 0;">Tarih: {surus_tarihi}</p>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 14px;">
                <tr>
                    <td><small style="color:#888">Sürücü:</small><br><b>{ad_soyad}</b></td>
                    <td style="text-align:right"><small style="color:#888">Bisiklet:</small><br><b>{bisiklet_modeli} ({bisiklet_kilosu}kg)</b></td>
                </tr>
            </table>
            
            <hr style="border: 0.5px solid #333; margin: 10px 0;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px;">
                <div style="background:#161B22; padding:8px; border-radius:8px;">
                    <small style="color:#888">KM Puanı ({surus_km} KM):</small><br><b style="color:#00D4FF">{km_puani}</b>
                </div>
                <div style="background:#161B22; padding:8px; border-radius:8px;">
                    <small style="color:#888">Rüzgar Primi ({ruzgar_hizi} km/h):</small><br><b style="color:#00D4FF">+{ruzgar_katkisi}</b>
                </div>
                <div style="background:#161B22; padding:8px; border-radius:8px;">
                    <small style="color:#888">Yükselti Primi ({yukselti} M):</small><br><b style="color:#00D4FF">+{yukselti_puani}</b>
                </div>
                <div style="background:#161B22; padding:8px; border-radius:8px;">
                    <small style="color:#888">Yakılan Yağ:</small><br><b style="color:#32CD32">{yakilan_yag} Gram</b>
                </div>
            </div>
            
            <div style="margin-top: 15px; background: #1F2937; padding: 12px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                <small style="color:#888; letter-spacing: 2px; font-size: 12px;">GENEL SÜRÜŞ SKORU</small>
                <h1 style="color: #FF4B4B; font-size: 48px; margin: 5px 0;">{final_puan}</h1>
                <small style="color:#fff; font-size: 12px;">Efor: {kalori} kcal</small>
            </div>
            
            <div style="margin-top: 15px; padding-top: 8px; border-top: 1px solid #333; display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                <b style="color: #FF4B4B;">Erkoz Yazılım Ar-Ge</b>
                <div style="text-align: right;">
                    <small style="color: #555;">Analiz Onay</small><br>
                    <span style="color: #EEE; font-size: 16px;"><i>Erdal Kozal</i></span>
                </div>
            </div>
        </div>
        """
        st.components.v1.html(cert_html, height=500, scrolling=False)
        st.success("Tebrikler kanka! Başarı belgen ve Excel kaydın pırıl pırıl hazır.")
    except:
        st.error("Bağlantı hatası! Excel'e yazılamadı.")

# --- YÖNETİCİ PANELİ ---
if st.session_state.is_admin:
    st.markdown("---")
    st.header("🏁 Erkoz Yönetici Paneli")
    st.markdown(f"""
        <a href="{SHEETS_LINK}" target="_blank">
            <button style="width:100%; height:80px; background-color:#FF4B4B; color:white; border:none; border-radius:15px; font-size:20px; font-weight:bold; cursor:pointer;">
                📊 TÜM GRUP LİSTESİNİ AÇ
            </button>
        </a>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
