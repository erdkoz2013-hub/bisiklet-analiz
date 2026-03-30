import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# ERKOZ ANALİZ v3.2 - BAŞLIK UYUMLU KESİN ÇÖZÜM
st.set_page_config(page_title="Erkoz Analiz", layout="centered")
st.title("🚴‍♂️ Erkoz Yazılım - Sürüş Analizi")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Z4WxyRA3Q3bUtvu29ZebnRIal10554fIQvut9uoVOZY/edit"

conn = st.connection("gsheets", type=GSheetsConnection)

def hesapla_erkoz_puani(km, ruzgar, yukselti):
    std_puan = 13.5
    km_puani = (std_puan / km) * 100
    ruzgar_puani = (km_puani * ruzgar) / 10
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    return round(km_puani + ruzgar_puani + yukselti_puani, 3)

st.subheader("📊 Yeni Sürüş Girişi")

with st.form("surus_formu"):
    tarih = st.date_input("Tarih", date.today())
    km = st.number_input("Mesafe (KM)", min_value=1.0, value=165.0)
    ruzgar = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=1.0)
    yukselti = st.number_input("Yükselti (Metre)", min_value=0, value=550)
    
    submit = st.form_submit_button("HESAPLA VE BULUTA KAYDET")

    if submit:
        try:
            puan = hesapla_erkoz_puani(km, ruzgar, yukselti)
            
            # Tablo başlıklarıyla birebir aynı isimleri kullanıyoruz
            yeni_veri = pd.DataFrame([{
                "Tarih": str(tarih),
                "KM": km,
                "Rüzgar": ruzgar,
                "Yukselti": yukselti,
                "Erkoz Puani": puan
            }])
            
            # Önce oku sonra ekle yöntemi (En güvenli)
            mevcut_veri = conn.read(spreadsheet=SHEET_URL)
            toplam_veri = pd.concat([mevcut_veri, yeni_veri], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=toplam_veri)
            
            st.success(f"✅ Kayıt Başarılı! Puanın: {puan}")
            st.balloons()
        except Exception as e:
            st.error(f"Hata detayı: {e}")
