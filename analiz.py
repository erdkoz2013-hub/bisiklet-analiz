import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# ERKOZ ANALİZ v3.0 - MOBİL & WEB SENKRONİZE
st.set_page_config(page_title="Erkoz Analiz", layout="centered")
st.title("🚴‍♂️ Erkoz Yazılım - Sürüş Analizi")

# BURAYA BİLGİSAYARDAKİ LİNKİ YAPIŞTIR
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Z4WxyRA3Q3bUtvu29ZebnRIal1O554fIQvut9uoVOZY/edit?usp=sharing" 

conn = st.connection("gsheets", type=GSheetsConnection)

def hesapla_erkoz_puani(km, ruzgar, yukselti):
    std_puan = 13.5 # Senin Excel'deki meşhur sabit puanın
    km_puani = (std_puan / km) * 100
    ruzgar_puani = (km_puani * ruzgar) / 10
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    return round(km_puani + ruzgar_puani + yukselti_puani, 3)

st.subheader("📊 Yeni Sürüş Girişi")
with st.form("surus_form"):
    tarih = st.date_input("Tarih", date.today())
    km = st.number_input("Mesafe (KM)", value=165.0)
    ruzgar = st.number_input("Rüzgar Hızı (km/h)", value=1.0)
    yukselti = st.number_input("Yükselti (Metre)", value=550)
    submit = st.form_submit_button("HESAPLA VE BULUTA KAYDET")

if submit:
    skor = hesapla_erkoz_puani(km, ruzgar, yukselti)
    yeni_veri = pd.DataFrame([{"Tarih": str(tarih), "KM": km, "Ruzgar": ruzgar, "Yukselti": yukselti, "Skor": skor}])
    
    try:
        mevcut = conn.read(spreadsheet=SHEET_URL)
        guncel = pd.concat([mevcut, yeni_veri], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=guncel)
        st.success(f"Kayıt Başarılı! Skor: {skor}")
        st.balloons()
    except:
        st.error("Bağlantı hatası! Lütfen Google Sheets linkini kontrol et.")

st.markdown("---")
st.subheader("📜 Geçmiş Sürüşler")
try:
    data = conn.read(spreadsheet=SHEET_URL)
    st.dataframe(data.tail(5), use_container_width=True)
except:
    st.write("Veri bekleniyor...")
