import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v17.0 - TAM ENTEGRASYON (VKE + RÜZGAR KADEME + TAM VERİ)
st.set_page_config(page_title="Erkoz Analiz v17.0", layout="wide", page_icon="🚴‍♂️")

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Analiz")
st.markdown("---")

# Senin Google Apps Script Linkin
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- ERKOZ MATEMATİKSEL MODELİ ---

def ruzgar_kademesi_bul(hiz):
    """0-15: 1, 16-30: 2, 31+: 3"""
    if hiz <= 15: return 1
    elif hiz <= 30: return 2
    else: return 3

def hesapla_standart_puan(yas, haftalik_km, beslenme_duzeyi, vke_puani):
    # Standart Excel Formülleri
    yas_puani = ((yas + 20) / 100) * 3
    antrenman_puani = (haftalik_km / 100) * 1.5
    enerji_puani = (beslenme_duzeyi / 1) * 1.3
    return round(yas_puani + antrenman_puani + enerji_puani + vke_puani, 3)

def hesapla_surus_puani(surus_km, ruzgar_hizi, yukselti, standart_puan):
    # 1. KM PUANI
    km_puani = (standart_puan / surus_km) * 100
    # 2. RÜZGAR KATKISI (Bölme Mantığı)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    ruzgar_katkisi = (km_puani / 10) * kademe 
    # 3. YÜKSELTI PUANI
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    
    return round(km_puani + ruzgar_katkisi + yukselti_puani, 3)

# --- ARAYÜZ TASARIMI ---

st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", min_value=100, value=179)
kilo = st.sidebar.number_input("Kilo (kg)", min_value=30.0, value=69.0, step=0.1)

# VKE HESAPLAMA VE GÖSTERİM
boy_m = boy / 100
vke = round(kilo / (boy_m * boy_m), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.markdown(f"💡 *VKE:* {vke} | *Puan Katkısı:* +{vke_katkisi}")
st.sidebar.write("---")

bisiklet_modeli = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Kilosu (kg)", min_value=1.0, value=15.0, step=0.1)
haftalik_km_input = st.sidebar.number_input("Haftalık Ortalama KM", min_value=0, value=200)
beslenme_input = st.sidebar.number_input("Beslenme Düzeyi (1-3)", min_value=1, max_value=3, value=3)

# Standart Puan Hesaplama
bugun = date.today()
yas = bugun.year - dogum_tarihi.year - ((bugun.month, bugun.day) < (dogum_tarihi.month, dogum_tarihi.day))
std_puan = hesapla_standart_puan(yas, haftalik_km_input, beslenme_input, vke_katkisi)
st.sidebar.info(f"📊 Toplam Standart Puan: *{std_puan}*")

# ANA EKRAN
col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", min_value=1.0, value=100.0)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=25.0)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    st.caption(f"⚡ Zorluk Kademesi: *{kademe}*")
    yukselti = st.number_input("Yükselti Kazanımı (m)", min_value=0, value=1049)

st.write("---")

if st.button("🚀 HESAPLA VE TABLOYA KAYDET"):
    final_puan = hesapla_surus_puani(surus_km, ruzgar_hizi, yukselti, std_puan)
    
    # GOOGLE SHEETS İÇİN VERİ PAKETİ (İsimler Kod.gs ile Tam Uyumlu)
    payload = {
        "adSoyad": ad_soyad,
        "dogumTarihi": str(dogum_tarihi),
        "boy": boy,
        "kilo": kilo,
        "bisikletModeli": bisiklet_modeli,
        "bisikletKilosu": bisiklet_kilosu,
        "haftalikKM": haftalik_km_input,
        "beslenmeDuzeyi": beslenme_input,
        "surusTarihi": str(surus_tarihi),
        "surusKM": surus_km,
        "ruzgar": ruzgar_hizi,
        "yukselti": yukselti,
        "surusPuani": final_puan
    }
    
    try:
        with st.spinner('Veriler Erkoz Bulutuna fırlatılıyor...'):
            res = requests.post(SCRIPT_URL, json=payload)
        if res.status_code == 200:
            st.success(f"✅ Her şey hazır! Tabloya tüm veriler gitti. Puan: {final_puan}")
            st.balloons()
        else:
            st.error("Google tarafında bir hata oluştu. Linki kontrol edin.")
    except:
        st.error("Bağlantı hatası.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
