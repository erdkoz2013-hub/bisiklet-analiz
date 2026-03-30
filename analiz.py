import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v8.0 - TAM PROFİL VE SÜRÜŞ ARŞİVİ
st.set_page_config(page_title="Erkoz Analiz v8.0", layout="wide", page_icon="🚴‍♂️")

st.title("🚴‍♂️ Erkoz Yazılım - Tam Sürüş Analizi")
st.markdown("---")

# Yeni gönderdiğin linki buraya tanımladım kanka
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- ERKOZ FORMÜLLERİ (EXCEL MANTIĞI) ---

def hesapla_standart_puan(dogum_tar, haftalik_km, beslenme_duzeyi):
    # Yaş Hesaplama
    bugun = date.today()
    yas = bugun.year - dogum_tar.year - ((bugun.month, bugun.day) < (dogum_tar.month, dogum_tar.day))
    # Excel Formülün: ((YAŞ+20)/100)*3
    yas_puani = ((yas + 20) / 100) * 3
    # Antrenman Puanı: (KM/100)*1,5
    antrenman_puani = (haftalik_km / 100) * 1.5
    # Enerji Puanı: (Beslenme/1)*1,3
    enerji_puani = (beslenme_duzeyi / 1) * 1.3
    
    return round(yas_puani + antrenman_puani + enerji_puani, 3)

def hesapla_surus_puani(surus_km, ruzgar_hizi, yukselti, standart_puan):
    # KM Puanı: (Standart puan / KM) * 100
    km_puani = (standart_puan / surus_km) * 100
    # Rüzgar Puanı: (Km puanı x Rüzgar hızı) / 10
    ruzgar_puani = (km_puani * ruzgar_hizi) / 10
    # Yükselti Puanı: (Yükselti / 1000 * 0,3) + 1
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    
    return round(km_puani + ruzgar_puani + yukselti_puani, 3)

# --- ARAYÜZ TASARIMI ---

# SOL MENÜ: PROFİL BİLGİLERİ
st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", min_value=100, value=179)
kilo = st.sidebar.number_input("Kilo (kg)", min_value=30.0, value=69.0, step=0.1)
bisiklet_modeli = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Kilosu (kg)", min_value=1.0, value=15.0, step=0.1)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", min_value=0, value=200)
beslenme = st.sidebar.selectbox("Beslenme Düzeyi", options=[1, 2, 3], index=2, help="1: Orta, 2: Yüksek, 3: Çok Yüksek")

# Standart Puan Hesapla
std_puan = hesapla_standart_puan(dogum_tarihi, haftalik_km, beslenme)
st.sidebar.info(f"📊 Mevcut Standart Puanınız: *{std_puan}*")

# ANA EKRAN: SÜRÜŞ VERİLERİ
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", min_value=1.0, value=165.0, step=0.1)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=1.0, step=0.1)
    yukselti = st.number_input("Yükselti Kazanımı (m)", min_value=0, value=550)

st.write("---")

if st.button("🚀 HESAPLA VE TABLOYA KAYDET"):
    # Hesaplamayı yap
    final_puan = hesapla_surus_puani(surus_km, ruzgar, yukselti, std_puan)
    
    # Google Sheets'e gidecek veri paketi
    payload = {
        "adSoyad": ad_soyad,
        "dogumTarihi": str(dogum_tarihi),
        "boy": boy,
        "kilo": kilo,
        "bisikletModeli": bisiklet_modeli,
        "bisikletKilosu": bisiklet_kilosu,
        "haftalikKM": haftalik_km,
        "beslenmeDuzeyi": beslenme,
        "surusTarihi": str(surus_tarihi),
        "surusKM": surus_km,
        "ruzgar": ruzgar,
        "yukselti": yukselti,
        "surusPuani": final_puan
    }
    
    try:
        with st.spinner('Veriler Erkoz Bulutuna işleniyor...'):
            res = requests.post(SCRIPT_URL, json=payload)
        
        if res.status_code == 200:
            st.success(f"✅ Kayıt Başarılı! Bu Sürüş İçin Puanınız: {final_puan}")
            st.balloons()
            st.write(f"*Özet:* {ad_soyad} için {surus_tarihi} tarihli, {surus_km} KM'lik sürüş başarıyla Excel'e işlendi.")
        else:
            st.error("Bağlantı sağlandı ancak Google Sheets tarafında bir hata oluştu.")
    except:
        st.error("Google servislerine ulaşılamıyor. Lütfen linki ve internetinizi kontrol edin.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Profesyonel Sürüş Analiz Sistemi")
