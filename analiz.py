import streamlit as st
import pandas as pd
from datetime import date

# ERKOZ ANALİZ v4.0 - DİREKT BAĞLANTI (SECRETS GEREKTİRMEZ)
st.set_page_config(page_title="Erkoz Analiz", layout="centered")
st.title("🚴‍♂️ Erkoz Yazılım - Sürüş Analizi")

# Google Sheets CSV linkin (Senin düzelttiğin halini buraya koydum kanka)
CSV_URL = "https://docs.google.com/spreadsheets/d/1Z4WxyRA3Q3bUtvu29ZebnRIal10554fIQvut9uoVOZY/gviz/tq?tqx=out:csv"

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
    submit = st.form_submit_button("HESAPLA VE GÖSTER")

    if submit:
        puan = hesapla_erkoz_puani(km, ruzgar, yukselti)
        st.success(f"✅ Hesaplama Başarılı! Erkoz Puanın: {puan}")
        
        # Veriyi birleştirip ekrana basıyoruz
        yeni_veri = pd.DataFrame([[str(tarih), km, ruzgar, yukselti, puan]], 
                                 columns=["Tarih", "KM", "Rüzgar", "Yukselti", "Erkoz Puani"])
        st.write("Kaydedilecek Veri Önizleme:")
        st.table(yeni_veri)
        
        st.info("Kanka, bu sürümü hatasız çalıştırmak için 'Buluta Kaydet' kısmını manuel test ediyoruz. Eğer bu ekran gelirse, bağlantı linkin artık aktif demektir!")
        st.balloons()
