import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴", layout="wide")

# 2. Veritabanı Fonksiyonları
dosya_adi = "erkoz_lig_final.csv"

def veriyi_kaydet(ad, puan, yag, kalori, vke):
    simdi = datetime.now()
    tarih_tam = simdi.strftime("%Y-%m-%d %H:%M")
    ay_yil = simdi.strftime("%B %Y")
    yeni_veri = pd.DataFrame([[ad, puan, yag, kalori, vke, ay_yil, tarih_tam]], 
                             columns=["Sürücü", "Puan", "Yağ (g)", "Kalori", "VKE", "Ay", "Tarih"])
    if not os.path.isfile(dosya_adi):
        yeni_veri.to_csv(dosya_adi, index=False)
    else:
        yeni_veri.to_csv(dosya_adi, mode='a', header=False, index=False)

def son_kaydi_sil():
    if os.path.isfile(dosya_adi):
        df = pd.read_csv(dosya_adi)
        if not df.empty:
            df[:-1].to_csv(dosya_adi, index=False)
            return True
    return False

# --- SOL TARAFA (SIDEBAR) TÜM VERİ GİRİŞLERİ ---
with st.sidebar:
    st.markdown("### 🛠️ Yönetici Paneli")
    admin_onay = st.checkbox("Düzenleme Kilidini Aç")
    if admin_onay:
        c1, c2 = st.columns(2)
        if c1.button("❌ Son Sil"):
            if son_kaydi_sil(): st.rerun()
        if c2.button("🗑️ Sıfırla"):
            if os.path.isfile(dosya_adi): os.remove(dosya_adi); st.rerun()
    
    st.markdown("---")
    st.header("📋 Veri Girişi")
    surucu_adi = st.text_input("Sürücü Adı Soyadı", "Erdal Kozal").strip()
    bisiklet_marka = st.text_input("Bisiklet Modeli", "Mosso Black Edition 29")
    
    st.markdown("---")
    st.subheader("⌚ Sürüş & Vücut Verileri")
    saat_kalori = st.number_input("Cihaz Kalorisi (Opsiyonel)", min_value=0, value=0)
    
    col_boy, col_kilo = st.columns(2)
    with col_boy:
        boy = st.number_input("Boy (m)", 1.0, 2.5, 1.75)
    with col_kilo:
        kilo = st.number_input("Kilo (kg)", 30.0, 200.0, 80.0)
    
    yas = st.number_input("Yaşınız", 10, 100, 60)
    
    st.markdown("🔥 *Sürüş Şiddeti*")
    kalori_seviyesi = st.selectbox("Şiddet", ["Az Kalori (Keyfi)", "Normal Kalori (Tempo)", "Çok Kalori (Performans)"], index=1, label_visibility="collapsed")
    
    st.markdown("🌬️ *İzmir Rüzgar Sertliği*")
    ruzgar_sertligi = st.select_slider("Rüzgar", options=["Sakin", "Tatlı Sert", "Yamanlar Esintisi", "Urla Fırtınası"], value="Tatlı Sert", label_visibility="collapsed")
    
    st.markdown("---")
    haftalik_km = st.number_input("Haftalık KM", 0, 1000, 255)
    haftalik_irtifa = st.number_input("Haftalık İrtifa (m)", 0, 5000, 1049)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 12.0)
    ruzgar_pozisyonu = st.selectbox("Grup Pozisyonu", ["Solo", "Kahraman (Önde)", "Takipçi"])

# --- SAĞ TARAF (ANA EKRAN) ---
st.title("🚴 Erkoz Hakkaniyetli Analiz & Şampiyonlar Ligi")

# Gelişmiş Hakkaniyet Algoritması (VKE Dahil)
vke = round(kilo / (boy ** 2), 1)
vke_bonusu = 1.0 + ((vke - 25.0) / 20.0) if vke >= 25.0 else 1.0

agirlik_katsayisi = bisiklet_agirligi / 7.0 
ruzgar_bonusu = 1.30 if "Kahraman" in ruzgar_pozisyonu else 1.0
yas_bonusu = 1.0 + (yas / 100) 
kalori_carpan = {"Az Kalori (Keyfi)": 1.0, "Normal Kalori (Tempo)": 1.15, "Çok Kalori (Performans)": 1.35}[kalori_seviyesi]
ruzgar_carpan = {"Sakin": 1.0, "Tatlı Sert": 1.10, "Yamanlar Esintisi": 1.20, "Urla Fırtınası": 1.40}[ruzgar_sertligi]

final_skor = int(((haftalik_km * 0.5) + (haftalik_irtifa * 0.1)) * agirlik_katsayisi * vke_bonusu * ruzgar_bonusu * yas_bonusu * kalori_carpan * ruzgar_carpan)
toplam_kalori = saat_kalori if saat_kalori > 0 else int(haftalik_km * 35 + haftalik_irtifa * 0.5)
yakilan_yag = round((toplam_kalori * 0.4) / 9, 1)

if st.button("🚀 Raporu Oluştur ve Lige Kaydol"):
    if surucu_adi:
        veriyi_kaydet(surucu_adi, final_skor, yakilan_yag, toplam_kalori, vke)
        st.balloons()
        
        # --- SERTİFİKA TASARIMI (TARİHLİ) ---
        simdi = datetime.now()
        tarih_ekran = simdi.strftime("%d.%m.%Y")
        tarih_saat_kod = simdi.strftime("%d%m%y-%H%M")
        
        st.markdown(f"""
        <div style="border: 5px solid #F35C5C; border-radius: 15px; background-color: white; padding: 20px; max-width: 480px; margin: 20px auto; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <div style="text-align: center;">
                <span style="font-size: 40px;">🏆</span>
                <h1 style="color: #F35C5C; margin: 0; font-size: 26px; font-weight: 900;">ERKOZ PERFORMANS SERTİFİKASI</h1>
                <p style="color: #888; font-size: 13px; margin: 5px 0;">Lisans No: 6012EXTREM-{tarih_saat_kod}</p>
                <hr style="border: 0.5px solid #eee;">
            </div>
            <div style="color: #333; font-size: 16px; padding: 10px; line-height: 1.6;">
                <b>Sürücü:</b> {surucu_adi}<br>
                <b>Ekipman:</b> {bisiklet_marka} ({bisiklet_agirligi} kg)<br>
                <b>VKE / Yaş:</b> {vke} Pts / {yas} Yaş<br>
                <b>Enerji:</b> {toplam_kalori} kcal / {yakilan_yag}g yağ
            </div>
            <div style="background-color: #38761D; color: white; border-radius: 10px; text-align: center; padding: 15px;">
                <div style="font-size: 12px; letter-spacing: 1px;">HAKKANİYETLİ BAŞARI PUANI</div>
                <div style="font-size: 60px; font-weight: 900; margin: 0;">{final_skor}</div>
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <p style="font-size: 12px; color: #777; margin-bottom: 5px;">Düzenleme Tarihi: <b>{tarih_ekran}</b></p>
                <div style="font-style: italic; font-size: 11px; color: #555;">
                    "Hafif bisikletle herkes gider, asıl başarı ağırla rüzgarı yenip bu yamaçta var olan emektir."<br>
                    <b>- Yamanlar, İzmir 2026 -</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ŞAMPİYONLAR LİGİ
st.markdown("---")
mevcut_ay = datetime.now().strftime("%B %Y")
st.header(f"🏆 Şampiyonlar Ligi - {mevcut_ay}")

if os.path.isfile(dosya_adi):
    df = pd.read_csv(dosya_adi)
    if not df.empty:
        aylik_df = df[df['Ay'] == mevcut_ay].sort_values(by="Puan", ascending=False).reset_index(drop=True)
        aylik_df.index += 1
        st.table(aylik_df[["Sürücü", "Puan", "VKE", "Kalori", "Tarih"]].head(10))