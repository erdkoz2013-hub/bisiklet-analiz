import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴", layout="wide")

# 2. Veritabanı Fonksiyonları
dosya_adi = "erkoz_final_v5.csv"

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

# --- SIDEBAR (VERİ GİRİŞİ) ---
with st.sidebar:
    st.button("🔄 Verileri Yenile", on_click=lambda: st.cache_data.clear())
    st.markdown("### 🛠️ Yönetici Paneli")
    admin = st.checkbox("Düzenleme Kilidini Aç")
    if admin:
        if st.button("❌ Son Kaydı Sil"):
            df = veriyi_oku()
            if not df.empty:
                df[:-1].to_csv(dosya_adi, index=False)
                st.cache_data.clear()
                st.rerun()
    
    st.header("📋 Veri Girişi")
    surucu_adi = st.text_input("Sürücü Adı Soyadı", "Erdal Kozal")
    bisiklet_marka = st.text_input("Ekipman", "Scott Addict 10")
    
    col_b, col_k = st.columns(2)
    with col_b: boy = st.number_input("Boy (m)", 1.0, 2.5, 1.75)
    with col_k: kilo = st.number_input("Kilo (kg)", 30.0, 200.0, 80.0)
    
    yas = st.number_input("Yaş", 10, 100, 60)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 12.0)
    
    st.markdown("🔥 *Sürüş Şiddeti*")
    kalori_sev = st.selectbox("Seviye", ["Az Kalori", "Normal Kalori", "Çok Kalori"], index=1)
    
    st.markdown("🌬️ *Rüzgar Sertliği*")
    ruzgar_sert = st.select_slider("Sertlik", options=["Sakin", "Tatlı Sert", "Yamanlar", "Urla"], value="Tatlı Sert")

# --- HESAPLAMALAR ---
vke = round(kilo / (boy ** 2), 1)
vke_bonusu = 1.0 + ((vke - 25.0) / 20.0) if vke >= 25.0 else 1.0
puan = int((624 * vke_bonusu * (bisiklet_agirligi / 12.0)) * (yas/60)) # Örnek katsayı
toplam_kalori = int(puan * 1.5)
yakilan_yag = round((toplam_kalori * 0.4) / 9, 1)

# --- ANA EKRAN ---
st.title("🚴 Erkoz Performans Sistemi")

if st.button("🚀 Sertifikayı Oluştur"):
    veriyi_kaydet(surucu_adi, puan, yakilan_yag, toplam_kalori, vke)
    tarih_kod = datetime.now().strftime("%d%m%y-%H%M")
    
    # SENİN İSTEDİĞİN DOLU TASARIM
    st.markdown(f"""
    <div style="border: 5px solid #F35C5C; border-radius: 15px; background-color: white; padding: 25px; max-width: 500px; margin: auto; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <div style="text-align: center;">
            <h1 style="color: #F35C5C; margin: 0; font-size: 28px; font-weight: 900;">ERKOZ SERTİFİKASI</h1>
            <p style="color: #666; font-size: 14px; margin-top: 5px;">Lisans: 6012EXTREM-{tarih_kod}</p>
            <hr style="border: 0.5px solid #eee;">
        </div>
        <div style="color: #333; font-size: 16px; padding: 15px 0; line-height: 1.8;">
            <b>Sürücü:</b> {surucu_adi}<br>
            <b>Ekipman:</b> {bisiklet_marka} ({bisiklet_agirligi} kg)<br>
            <b>Vücut Verisi:</b> {vke} VKE / {yas} Yaş<br>
            <b>Enerji:</b> {toplam_kalori} kcal / {yakilan_yag}g yağ
        </div>
        <div style="background-color: #38761D; color: white; border-radius: 10px; text-align: center; padding: 20px;">
            <div style="font-size: 14px; letter-spacing: 1px; opacity: 0.9;">HAKKANİYETLİ BAŞARI PUANI</div>
            <div style="font-size: 65px; font-weight: 900; margin: 0;">{puan}</div>
        </div>
        <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #888;">
            Düzenleme: {datetime.now().strftime('%d.%m.%Y')}<br>
            <i>"Asıl başarı ağırla rüzgarı yenip bu yamaçta var olan emektir."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ŞAMPİYONLAR LİGİ
st.markdown("---")
st.header("🏆 Şampiyonlar Ligi")
df_liste = veriyi_oku()
if not df_liste.empty:
    # Tabloyu da senin görselindeki gibi düzenleyelim
    st.table(df_liste.sort_values(by="Puan", ascending=False).head(10))