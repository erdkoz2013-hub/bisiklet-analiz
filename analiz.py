import streamlit as st
import pandas as pd
from datetime import date
import requests

# ERKOZ ANALİZ v15.0 - EXCEL BÖLME MANTIĞI (TAM UYUM)
st.set_page_config(page_title="Erkoz Analiz v15.0", layout="wide", page_icon="🚴‍♂️")

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

def hesapla_surus_puani(surus_km, ruzgar_hizi, yukselti, standart_puan):
    # 1. KM PUANI (Senin tablodaki 12.247 olan değer)
    km_puani = (standart_puan / surus_km) * 100
    
    # 2. RÜZGAR KATKISI (Senin formül: KM Puanı / Kademe / 10 * Kademe gibi bir mantık)
    # 1 kademe -> 1.225 katkı | 2 kademe -> 2.449 katkı | 3 kademe -> 3.674 katkı
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    # Senin Excel'deki o "bölme" ve kademeye göre artış mantığı tam olarak şuna denk geliyor:
    ruzgar_katkisi = (km_puani / 10) * kademe 
    
    # 3. YÜKSELTI PUANI
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    
    return round(km_puani + ruzgar_katkisi + yukselti_puani, 3)

# --- ARAYÜZ ---

st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", min_value=100, value=179)
kilo = st.sidebar.number_input("Kilo (kg)", min_value=30.0, value=69.0, step=0.1)

boy_m = boy / 100
vke = round(kilo / (boy_m * boy_m), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.markdown(f"💡 *VKE:* {vke} | *Puan Katkısı:* +{vke_katkisi}")
st.sidebar.write("---")

bisiklet_modeli = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Kilosu (kg)", min_value=1.0, value=15.0, step=0.1)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", min_value=0, value=200)
beslenme = st.sidebar.number_input("Beslenme Düzeyi (1-3)", min_value=1, max_value=3, value=2)

yas = date.today().year - dogum_tarihi.year
std_puan = hesapla_standart_puan(yas, haftalik_km, beslenme, vke_katkisi)
st.sidebar.info(f"📊 Standart Puan: *{std_puan}*")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", min_value=1.0, value=100.0, step=0.1)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi_input = st.number_input("Rüzgar Hızı (km/h)", min_value=0.0, value=25.0, step=0.1)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi_input)
    st.caption(f"⚡ Kademe: *{kademe}* | Beklenen Katkı: *~{round((std_puan/surus_km*100/10)*kademe, 3)}*")
    yukselti = st.number_input("Yükselti Kazanımı (m)", min_value=0, value=1049)

st.write("---")

if st.button("🚀 HESAPLA VE TABLOYA KAYDET"):
    final_puan = hesapla_surus_puani(surus_km, ruzgar_hizi_input, yukselti, std_puan)
    
    payload = {
        "adSoyad": ad_soyad, "dotar": str(dogum_tarihi), "boy": boy, "kilo": kilo,
        "bisiklet": bisiklet_modeli, "b_kilo": bisiklet_kilosu, "h_km": haftalik_km,
        "beslenme": beslenme, "s_tarih": str(surus_tarihi), "s_km": surus_km,
        "ruzgar": ruzgar_hizi_input, "yukselti": yukselti, "puan": final_puan
    }
    
    try:
        res = requests.post(SCRIPT_URL, json=payload)
        if res.status_code == 200:
            st.success(f"✅ Kayıt Başarılı! Excel Puanın: {final_puan}")
            st.balloons()
    except:
        st.error("Bağlantı hatası.")
