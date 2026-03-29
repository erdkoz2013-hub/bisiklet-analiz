import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴", layout="wide")

# 2. Veritabanı Fonksiyonları
dosya_adi = "erkoz_performans_v6.csv"

def veriyi_oku():
    if os.path.isfile(dosya_adi):
        return pd.read_csv(dosya_adi)
    return pd.DataFrame(columns=["Sürücü", "Puan", "Yağ (g)", "Kalori", "VKE", "Ay", "Tarih"])

def veriyi_kaydet(ad, puan, yag, kalori, vke):
    simdi = datetime.now()
    tarih_tam = simdi.strftime("%Y-%m-%d %H:%M")
    ay_yil = simdi.strftime("%B %Y")
    yeni_satir = pd.DataFrame([[ad, puan, yag, kalori, vke, ay_yil, tarih_tam]], 
                             columns=["Sürücü", "Puan", "Yağ (g)", "Kalori", "VKE", "Ay", "Tarih"])
    if not os.path.isfile(dosya_adi):
        yeni_satir.to_csv(dosya_adi, index=False)
    else:
        yeni_satir.to_csv(dosya_adi, mode='a', header=False, index=False)
    st.cache_data.clear()

# --- SIDEBAR (VERİ GİRİŞİ VE YÖNETİCİ PANELİ) ---
with st.sidebar:
    st.button("🔄 Verileri Eşitle", on_click=lambda: st.cache_data.clear())
    
    st.markdown("### 🛠️ Yönetici Paneli")
    admin = st.checkbox("Düzenleme Yetkisini Aç")
    if admin:
        col_admin1, col_admin2 = st.columns(2)
        with col_admin1:
            if st.button("❌ Son Kaydı Sil"):
                df = veriyi_oku()
                if not df.empty:
                    df[:-1].to_csv(dosya_adi, index=False)
                    st.cache_data.clear(); st.rerun()
        with col_admin2:
            if st.button("🗑️ Hepsini Sil"): # İstediğin o nükleer buton
                if os.path.isfile(dosya_adi):
                    os.remove(dosya_adi)
                    st.cache_data.clear(); st.rerun()
    
    st.markdown("---")
    st.header("📋 Sürücü Bilgileri")
    surucu_adi = st.text_input("Ad Soyad", "Erdal Kozal")
    ekipman = st.text_input("Bisiklet Modeli", "Scott Addict 10")
    
    col_boy, col_kilo = st.columns(2)
    with col_boy: boy = st.number_input("Boy (m)", 1.0, 2.5, 1.75)
    with col_kilo: kilo = st.number_input("Kilo (kg)", 30.0, 200.0, 80.0)
    
    yas = st.number_input("Yaş", 10, 100, 60)
    
    st.markdown("---")
    # Huawei saatinden gelen toplam kaloriyi buraya giriyoruz
    huawei_kalori = st.number_input("Huawei Toplam Kalori", min_value=0, value=0)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 12.0)
    
    st.markdown("🔥 *Sürüş Şiddeti*")
    kalori_sev = st.selectbox("Seviye", ["Az Kalori", "Normal Kalori", "Çok Kalori"], index=1)
    
    st.markdown("🌬️ *Rüzgar Sertliği*")
    ruzgar_sert = st.select_slider("İzmir Rüzgarı", options=["Sakin", "Tatlı Sert", "Yamanlar", "Urla"], value="Tatlı Sert")

# --- ADALETLİ HESAPLAMALAR ---
# Vücut Kitle Endeksi (VKE)
vke_hesap = round(kilo / (boy ** 2), 1)
vke_bonusu = 1.0 + ((vke_hesap - 25.0) / 20.0) if vke_hesap >= 25.0 else 1.0

# Puan Algoritması (Yaş, VKE ve Ağırlık çarpanı ile)
puan = int(624 * vke_bonusu * (bisiklet_agirligi / 12.0) * (yas / 60))

# Yağ Yakımı (Kalori üzerinden %40 verimle hesaplanır)
yakilan_yag = round((huawei_kalori * 0.4) / 9, 1)

# --- ANA EKRAN ---
st.title("🚴 Erkoz Hakkaniyetli Analiz")

if st.button("🚀 Sertifikayı Oluştur ve Kaydet"):
    veriyi_kaydet(surucu_adi, puan, yakilan_yag, huawei_kalori, vke_hesap)
    st.balloons()
    
    tarih_kod = datetime.now().strftime("%d%m%y-%H%M")
    
    # TAM DOLU SERTİFİKA TASARIMI
    st.markdown(f"""
    <div style="border: 5px solid #F35C5C; border-radius: 15px; background-color: white; padding: 25px; max-width: 500px; margin: auto; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <div style="text-align: center;">
            <h1 style="color: #F35C5C; margin: 0; font-size: 28px; font-weight: 900;">ERKOZ SERTİFİKASI</h1>
            <p style="color: #666; font-size: 14px; margin-top: 5px;">Lisans: 6012EXTREM-{tarih_kod}</p>
            <hr style="border: 0.5px solid #eee;">
        </div>
        <div style="color: #333; font-size: 16px; padding: 15px 0; line-height: 1.8;">
            <b>Sürücü:</b> {surucu_adi}<br>
            <b>Ekipman:</b> {ekipman} ({bisiklet_agirligi} kg)<br>
            <b>Vücut Verisi:</b> {vke_hesap} VKE / {yas} Yaş<br>
            <b>Enerji:</b> {huawei_kalori} kcal / {yakilan_yag}g yağ
        </div>
        <div style="background-color: #38761D; color: white; border-radius: 10px; text-align: center; padding: 20px;">
            <div style="font-size: 14px; letter-spacing: 1px;">HAKKANİYETLİ BAŞARI PUANI</div>
            <div style="font-size: 70px; font-weight: 900; margin: 0;">{puan}</div>
        </div>
        <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #888;">
            Düzenleme: {datetime.now().strftime('%d.%m.%Y')}<br>
            <i>"Asıl başarı ağırla rüzgarı yenip bu yamaçta var olan emektir."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# LİG TABLOSU
st.markdown("---")
st.header("🏆 Şampiyonlar Ligi")
df_liste = veriyi_oku()
if not df_liste.empty:
    st.table(df_liste.sort_values(by="Puan", ascending=False).head(10))