import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v24.0 - YAĞ YAKIM & ENERJİ GÜNCELLEMESİ
st.set_page_config(page_title="Erkoz Analiz v24.0", layout="wide", page_icon="🚴‍♂️")

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Analiz")
st.markdown("---")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- MOTOR ---
def ruzgar_kademesi_bul(hiz):
    if hiz <= 15: return 1
    elif hiz <= 30: return 2
    else: return 3

def hesapla_standart_puan(yas, haftalik_km, beslenme, vke_puani):
    return round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_puani, 3)

# --- ARAYÜZ ---
st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad = st.sidebar.text_input("Sürücü Adı Soyadı", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

vke = round(kilo / ((boy/100)**2), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.info(f"💡 VKE: {vke} | Katkı: +{vke_katkisi}")

bisiklet = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.number_input("Beslenme (1-3)", value=3)

yas = date.today().year - dogum_tarihi.year
std_puan = hesapla_standart_puan(yas, haftalik_km, beslenme, vke_katkisi)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=100.0)
    kalori = st.number_input("Yakılan Toplam Kalori", value=2500)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    yukselti = st.number_input("Yükselti (m)", value=1049)

if st.button("🚀 ANALİZİ VE YAĞ YAKIMINI KAYDET"):
    # Hesaplamalar
    km_puani = round((std_puan / surus_km) * 100, 3)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    
    # YAĞ YAKIM HESABI (Gram cinsinden)
    # Formül: (Kalori * 0.8) / 9
    yakilan_yag = round((kalori * 0.8) / 9, 1)
    
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)
    
    payload = {
        "adSoyad": ad_soyad, "dotar": str(dogum_tarihi), "boy": boy, "kilo": kilo,
        "bisiklet": bisiklet, "h_km": haftalik_km, "beslenme": beslenme,
        "s_tarih": str(surus_tarihi), "s_km": surus_km, "ruzgar": ruzgar_hizi,
        "yukselti": yukselti, "puan": final_puan, "kalori": kalori, "yag": yakilan_yag
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        cert_container = f"""
        <div style="background-color: #0E1117; border: 5px double #FF4B4B; padding: 20px; border-radius: 15px; font-family: sans-serif; color: white;">
            <h2 style="color: #FF4B4B; text-align: center; margin-top: 0;">🏆 ERKOZ PERFORMANS & YAĞ YAKIM ANALİZİ</h2>
            <p style="text-align: center; color: #888;">Tarih: {surus_tarihi}</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Mesafe: {surus_km} KM</small><br><b style="color:#00D4FF">Puan: {km_puani}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Rüzgar Mücadelesi</small><br><b style="color:#00D4FF">Primi: +{ruzgar_katkisi}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Tırmanış Gücü</small><br><b style="color:#00D4FF">Primi: +{yukselti_puani}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Yakılan Yağ Miktarı</small><br><b style="color:#32CD32">{yakilan_yag} Gram</b>
                </div>
            </div>
            
            <div style="margin-top: 20px; background: #1F2937; padding: 15px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                <p style="color:#888; margin:0; font-size: 14px;">Toplam Kalori: {kalori} kcal</p>
                <h1 style="color: #FF4B4B; font-size: 50px; margin: 5px 0;">{final_puan}</h1>
                <p style="color:white; font-size: 14px; letter-spacing: 2px;">GENEL SÜRÜŞ SKORU</p>
            </div>
            
            <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #333; display: flex; justify-content: space-between; align-items: center;">
                <b style="color: #FF4B4B; font-size: 14px;">Erkoz Yazılım Ar-Ge</b>
                <div style="text-align: right;">
                    <small style="color: #555;">Analiz Onay</small><br>
                    <span style="color: #EEE; font-size: 18px;"><i>Erdal Kozal</i></span>
                </div>
            </div>
        </div>
        """
        st.write("---")
        st.components.v1.html(cert_container, height=520, scrolling=False)
        st.success(f"Analiz tamamlandı. Bugün tam {yakilan_yag} gram yağa veda ettin kanka!")
    except:
        st.error("Bağlantı hatası.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
