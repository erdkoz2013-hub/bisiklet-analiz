import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v20.0 - İMZALI & MÜHÜRLÜ PRESTİJ VERSİYONU
st.set_page_config(page_title="Erkoz Analiz v20.0", layout="wide", page_icon="🚴‍♂️")

# İzmir temalı özel stil ayarları
st.markdown("""
    <style>
        .report-label { color: #A8B2BD; font-size: 14px; margin-bottom: -5px; }
        .report-value { color: #FFFFFF; font-size: 19px; font-weight: bold; margin-top: 0; }
        .report-contrib { color: #00D4FF; font-size: 15px; font-style: italic; }
        .score-box { background-color: #1F2937; padding: 15px; border-radius: 10px; border: 3px solid #FF4B4B; text-align: center; min-width: 200px; }
        .cert-header { color: #FF4B4B; text-align: center; margin-top: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 2px; }
        .signature-area { border-top: 1px solid #333; margin-top: 30px; padding-top: 15px; display: flex; justify-content: space-between; align-items: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Analiz")
st.markdown("---")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- ERKOZ MATEMATİKSEL MODELİ ---
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
        "final_puan": final_puan,
        "km_puani": round(km_puani, 3),
        "ruzgar_kademe": kademe,
        "ruzgar_katkisi": round(ruzgar_katkisi, 3),
        "yukselti_puani": round(yukselti_puani, 3)
    }

# --- ARAYÜZ TASARIMI ---
st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad_input = st.sidebar.text_input("Sürücü Adı Soyadı", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", min_value=100, value=179)
kilo = st.sidebar.number_input("Kilo (kg)", min_value=30.0, value=69.0, step=0.1)

boy_m = boy / 100
vke = round(kilo / (boy_m * boy_m), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.markdown(f"💡 *VKE:* {vke} | *Katkı:* +{vke_katkisi}")

bisiklet_modeli_input = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
haftalik_km_input = st.sidebar.number_input("Haftalık Ortalama KM", min_value=0, value=200)
beslenme_input = st.sidebar.number_input("Beslenme Düzeyi (1-3)", min_value=1, max_value=3, value=3)

bugun = date.today()
yas = bugun.year - dogum_tarihi.year - ((bugun.month, bugun.day) < (dogum_tarihi.month, dogum_tarihi.day))
std_puan = hesapla_standart_puan(yas, haftalik_km_input, beslenme_input, vke_katkisi)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km_input = st.number_input("Yapılan KM", min_value=1.0, value=100.0)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi_input = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=25.0)
    yukselti_input = st.number_input("Yükselti Kazanımı (m)", min_value=0, value=1049)

if st.button("🚀 ANALİZ ET VE KAYDET"):
    analiz = hesapla_surus_analizi(surus_km_input, ruzgar_hizi_input, yukselti_input, std_puan)
    final_puan = analiz["final_puan"]
    
    payload = {
        "adSoyad": ad_soyad_input, "dogumTarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo,
        "bisikletModeli": bisiklet_modeli_input, "bisikletKilosu": 15.0, "haftalikKM": haftalik_km_input,
        "beslenmeDuzeyi": beslenme_input, "surusTarihi": str(surus_tarihi), "surusKM": surus_km_input,
        "ruzgar": ruzgar_hizi_input, "yukselti": yukselti_input, "surusPuani": final_puan
    }
    
    try:
        res = requests.post(SCRIPT_URL, json=payload)
        if res.status_code == 200:
            st.balloons()
            
            # --- ERKOZ PRESTİJ SERTİFİKASI ---
            st.markdown(f"""
                <div style="border: 6px double #FF4B4B; padding: 35px; border-radius: 25px; background-color: #0E1117; font-family: sans-serif;">
                    <h1 class="cert-header">🏆 ERKOZ PERFORMANS ANALİZİ</h1>
                    <p style="text-align: center; color: #888; margin-top: -10px;">Sürüş Tarihi: {surus_tarihi}</p>
                    
                    <div style="display: flex; justify-content: space-between; margin: 30px 0;">
                        <div><p class="report-label">Sürücü</p><h2 class="report-value">{ad_soyad_input}</h2></div>
                        <div style="text-align: right;"><p class="report-label">Bisiklet</p><h2 class="report-value">{bisiklet_modeli_input}</h2></div>
                    </div>
                    
                    <hr style="border: 0.5px solid #333; margin: 20px 0;">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                        <div style="background: #161B22; padding: 15px; border-radius: 12px;">
                            <p class="report-label">Mesafe Etkisi</p>
                            <p class="report-value">{surus_km_input} KM</p>
                            <p class="report-contrib">Temel KM Puanı: {analiz["km_puani"]}</p>
                        </div>
                        <div style="background: #161B22; padding: 15px; border-radius: 12px;">
                            <p class="report-label">Rüzgar Mücadelesi</p>
                            <p class="report-value">{ruzgar_hizi_input} km/h (Kademe {analiz["ruzgar_kademe"]})</p>
                            <p class="report-contrib">Rüzgar Primi: +{analiz["ruzgar_katkisi"]}</p>
                        </div>
                        <div style="background: #161B22; padding: 15px; border-radius: 12px;">
                            <p class="report-label">Zirve Tırmanışı</p>
                            <p class="report-value">{yukselti_input} Metre</p>
                            <p class="report-contrib">İrtifa Primi: +{analiz["yukselti_puani"]}</p>
                        </div>
                        <div style="background: #161B22; padding: 15px; border-radius: 12px;">
                            <p class="report-label">Fiziksel Kondisyon (VKE)</p>
                            <p class="report-value">{vke} Endeks</p>
                            <p class="report-contrib">Fizik Avantajı: +{vke_katkisi}</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: center; margin: 40px 0;">
                        <div class="score-box">
                            <p style="color: white; margin-bottom: 5px; font-size: 18px; letter-spacing: 1px;">GENEL SÜRÜŞ SKORU</p>
                            <h1 style="color: #FF4B4B; font-size: 75px; margin: 0; font-family: 'Arial Black';">{final_puan}</h1>
                        </div>
                    </div>
                    
                    <div class="signature-area">
                        <div>
                            <p style="color: #555; font-size: 12px; margin: 0;">Sistem Sağlayıcı</p>
                            <p style="color: #FF4B4B; font-weight: bold; margin: 0;">Erkoz Yazılım Ar-Ge</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #555; font-size: 12px; margin: 0;">Analiz Onay ve İmza</p>
                            <p style="color: #FFFFFF; font-family: 'Brush Script MT', cursive; font-size: 24px; margin: 0;">Erdal Kozal</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.success("Tebrikler kanka! Sertifikan Erdal Kozal imzasıyla onaylandı.")
    except:
        st.error("Bağlantı hatası.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Performans Analiz ve Tescil Merkezi")
