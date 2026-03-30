import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v7.0 - TAM OTOMATİK SİSTEM
st.set_page_config(page_title="Erkoz Analiz", layout="centered", page_icon="🚴‍♂️")

st.title("🚴‍♂️ Erkoz Yazılım - Sürüş Analizi")
st.markdown("---")

# Senin Google Apps Script Linkin
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz4PX7fgUG6uEiGu_Y5aQ8d7kvHNybZvhKivP3bSCSHdL1KuNfais2bziK4Dnoilvi9-w/exec"

def hesapla_erkoz_puani(km, ruzgar, yukselti):
    std_puan = 13.5
    km_puani = (std_puan / km) * 100
    ruzgar_puani = (km_puani * ruzgar) / 10
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    return round(km_puani + ruzgar_puani + yukselti_puani, 3)

st.subheader("📊 Yeni Sürüş Girişi")

with st.form("surus_formu"):
    tarih = st.date_input("Tarih Seçin", date.today())
    km = st.number_input("Mesafe (KM)", min_value=1.0, value=165.0, step=0.1)
    ruzgar = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=1.0, step=0.1)
    yukselti = st.number_input("Yükselti Kazanımı (Metre)", min_value=0, value=550)
    
    st.write("---")
    submit = st.form_submit_button("HESAPLA VE BULUTA KAYDET")

    if submit:
        puan = hesapla_erkoz_puani(km, ruzgar, yukselti)
        
        # Google Sheets'e gönderilecek veri paketi
        payload = {
            "Tarih": str(tarih),
            "KM": km,
            "Rüzgar": ruzgar,
            "Yukselti": yukselti,
            "Puan": puan
        }
        
        try:
            # Veriyi Google'a fırlatıyoruz
            with st.spinner('Veri buluta gönderiliyor...'):
                response = requests.post(SCRIPT_URL, json=payload)
            
            if response.status_code == 200:
                st.success(f"✅ Başarıyla Kaydedildi! Erkoz Puanın: {puan}")
                st.balloons()
            else:
                st.error("Bağlantı başarılı ama veri yazılamadı.")
        except Exception as e:
            st.error(f"Bir hata oluştu: Bağlantı kurulamadı.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
