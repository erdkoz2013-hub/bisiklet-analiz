import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v21.0 - HATASIZ PRESTİJ BELGESİ
st.set_page_config(page_title="Erkoz Analiz v21.0", layout="wide", page_icon="🚴‍♂️")

# Görsel stil ayarlarını mühürleyelim
st.markdown("""
    <style>
        .report-label { color: #A8B2BD !important; font-size: 14px !important; margin-bottom: 2px !important; }
        .report-value { color: #FFFFFF !important; font-size: 19px !important; font-weight: bold !important; margin-top: 0 !important; }
        .report-contrib { color: #00D4FF !important; font-size: 15px !important; font-style: italic !important; }
        .score-box { background-color: #1F2937 !important; padding: 15px !important; border-radius: 10px !important; border: 3px solid #FF4B4B !important; text-align: center !important; }
        .cert-header { color: #FF4B4B !important; text-align: center !important; font-family: 'Arial Black', sans-serif !important; letter-spacing: 2px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Analiz")
st.markdown("---")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- MATEMATİKSEL MOTOR ---
def ruzgar_kademesi_bul(hiz):
    if hiz <= 15: return 1
    elif hiz <= 30: return 2
    else: return 3

def hesapla_standart_puan(yas, haftalik_km, beslenme_duzeyi, vke_puani):
    yas_puani = ((yas + 20) / 100) * 3
    antrenman_puani = (haftalik_km / 100) * 1.5
    enerji_puani = (beslenme_duzeyi / 1) * 1.3
    return round(yas_puani + antrenman_puani + enerji_puani + vke_puani, 3)

def hesapla_surus_analizi(surus_km, ruzgar_hizi, yukselti, standart_puan):
    km_puani = (standart_puan / surus_km) * 100
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    ruzgar_katkisi = (km_puani / 10) * kademe 
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani, 3)
    return {
        "final_puan": final_puan, "km_puani": round(km_puani, 3),
        "ruzgar_kademe": kademe, "ruzgar_katkisi": round(ruzgar_katkisi, 3),
        "yukselti_puani": round(yukselti_puani, 3)
    }

# --- ARAYÜZ ---
st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad_input = st.sidebar.text_input("Sürücü Adı Soyadı", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

vke = round(kilo / ((boy/100)**2), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.info(f"💡 VKE: {vke} | Katkı: +{vke_katkisi}")

bisiklet_modeli = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.number_input("Beslenme (1-3)", value=3)

bugun = date.today()
yas = bugun.year - dogum_tarihi.year
std_puan = hesapla_standart_puan(yas, haftalik_km, beslenme, vke_katkisi)

col1, col2 = st.columns(2)
with col1:
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=100.0)
with col2:
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    yukselti = st.number_input("Yükselti (m)", value=1049)

if st.button("🚀 ANALİZ ET VE BELGEYİ HAZIRLA"):
    analiz = hesapla_surus_analizi(surus_km, ruzgar_hizi, yukselti, std_puan)
    final_puan = analiz["final_puan"]
    
    payload = {
        "adSoyad": ad_soyad_input, "dogumTarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo,
        "bisikletModeli": bisiklet_modeli, "bisikletKilosu": 15.0, "haftalikKM": haftalik_km,
        "beslenmeDuzeyi": beslenme, "surusTarihi": str(surus_tarihi), "surusKM": surus_km,
        "ruzgar": ruzgar_hizi, "yukselti": yukselti, "surusPuani": final_puan
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # --- HATASIZ PRESTİJ SERTİFİKASI ---
        cert_html = f"""
        <div style="border: 6px double #FF4B4B; padding: 25px; border-radius: 20px; background-color: #0E1117; color: white;">
            <h2 style="color: #FF4B4B; text-align: center; margin-bottom: 5px;">🏆 ERKOZ PERFORMANS ANALİZİ</h2>
            <p style="text-align: center; color: #888; margin-bottom: 20px;">Sürüş Tarihi: {surus_tarihi}</p>
            
            <div style="display: flex; justify-content: space-between;">
                <div><small style="color: #888;">Sürücü</small><br><b>{ad_soyad_input}</b></div>
                <div style="text-align: right;"><small style="color: #888;">Bisiklet</small><br><b>{bisiklet_modeli}</b></div>
            </div>
            
            <hr style="border: 0.5px solid #333; margin: 15px 0;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background: #161B22; padding: 10px; border-radius: 8px;">
                    <small style="color: #888;">Mesafe: {surus_km} KM</small><br><span style="color: #00D4FF;">Temel: {analiz['km_puani']}</span>
                </div>
                <div style="background: #161B22; padding: 10px; border-radius: 8px;">
                    <small style="color: #888;">Rüzgar: {ruzgar_hizi} km/h</small><br><span style="color: #00D4FF;">Primi: +{analiz['ruzgar_katkisi']}</span>
                </div>
                <div style="background: #161B22; padding: 10px; border-radius: 8px;">
                    <small style="color: #888;">Yükselti: {yukselti} M</small><br><span style="color: #00D4FF;">Primi: +{analiz['yukselti_puani']}</span>
                </div>
                <div style="background: #161B22; padding: 10px; border-radius: 8px;">
                    <small style="color: #888;">VKE Endeks: {vke}</small><br><span style="color: #00D4FF;">Avantaj: +{vke_katkisi}</span>
                </div>
            </div>
            
            <div style="margin: 25px 0; text-align: center; background: #1F2937; padding: 20px; border-radius: 15px; border: 2px solid #FF4B4B;">
                <small style="letter-spacing: 2px;">GENEL SÜRÜŞ SKORU</small>
                <h1 style="color: #FF4B4B; font-size: 60px; margin: 0;">{final_puan}</h1>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #333; padding-top: 10px;">
                <span style="color: #FF4B4B; font-weight: bold; font-size: 14px;">Erkoz Yazılım Ar-Ge</span>
                <div style="text-align: right;">
                    <small style="color: #555; font-size: 10px;">Analiz Onay</small><br>
                    <span style="font-family: cursive; font-size: 20px; color: #EEE;">Erdal Kozal</span>
                </div>
            </div>
        </div>
        """
        st.markdown(cert_html, unsafe_allow_html=True)
        st.success("Analiz tamamlandı, imzan hazır kanka!")
    except:
        st.error("Bağlantı hatası.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Performans Analiz Merkezi")
