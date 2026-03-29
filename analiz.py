import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴", layout="wide")

# 2. Veritabanı ve Senkronizasyon Ayarı
# Dosya adını 'erkoz_v4_final.csv' olarak güncelledim ki sistem taze bir başlangıç yapsın
dosya_adi = "erkoz_v4_final.csv"

# ÖNEMLİ: Veriyi okurken cache (önbellek) oluşmaması için copy() kullanıyoruz
def veriyi_oku():
    if os.path.isfile(dosya_adi):
        # Dosyayı her seferinde diskten taze oku
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
    st.cache_data.clear() # Önbelleği zorla temizle

def son_kaydi_sil():
    df = veriyi_oku()
    if not df.empty:
        df[:-1].to_csv(dosya_adi, index=False)
        st.cache_data.clear() # Silme sonrası önbelleği temizle
        return True
    return False

# --- SIDEBAR (SOL MENÜ) ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    
    # TELEFON VE PC ARASINDAKİ FARKI ÇÖZMEK İÇİN YENİLE BUTONU
    if st.button("🔄 Verileri Senkronize Et (Zorla Yenile)"):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🛠️ Yönetici Paneli")
    admin_onay = st.checkbox("Düzenleme Kilidini Aç")
    if admin_onay:
        c1, c2 = st.columns(2)
        if c1.button("❌ Son Sil"):
            if son_kaydi_sil(): st.rerun()
        if c2.button("🗑️ Sıfırla"):
            if os.path.isfile(dosya_adi): 
                os.remove(dosya_adi)
                st.cache_data.clear()
                st.rerun()
    
    st.markdown("---")
    st.header("📋 Veri Girişi")
    surucu_adi = st.text_input("Sürücü Adı Soyadı", "Erdal Kozal").strip()
    bisiklet_marka = st.text_input("Bisiklet Modeli", "Mosso Black Edition29")
    
    col_boy, col_kilo = st.columns(2)
    with col_boy: boy = st.number_input("Boy (m)", 1.0, 2.5, 1.75)
    with col_kilo: kilo = st.number_input("Kilo (kg)", 30.0, 200.0, 80.0)
    
    yas = st.number_input("Yaşınız", 10, 100, 60)
    
    st.markdown("🔥 *Sürüş Şiddeti*")
    kalori_seviyesi = st.selectbox("Şiddet", ["Az Kalori", "Normal Kalori", "Çok Kalori"], index=1)
    
    st.markdown("🌬️ *Rüzgar Sertliği*")
    ruzgar_sertligi = st.select_slider("Rüzgar", options=["Sakin", "Tatlı Sert", "Yamanlar", "Urla"], value="Tatlı Sert")
    
    st.markdown("---")
    haftalik_km = st.number_input("Haftalık KM", 0, 1000, 255)
    haftalik_irtifa = st.number_input("Haftalık İrtifa (m)", 0, 5000, 1049)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 12.0)
    ruzgar_pozisyonu = st.selectbox("Grup Pozisyonu", ["Solo", "Kahraman", "Takipçi"])

# --- ANA EKRAN ---
st.title("🚴 Erkoz Hakkaniyetli Analiz")

# Hesaplamalar
vke = round(kilo / (boy ** 2), 1)
vke_bonusu = 1.0 + ((vke - 25.0) / 20.0) if vke >= 25.0 else 1.0
puan = int(((haftalik_km * 0.5) + (haftalik_irtifa * 0.1)) * (bisiklet_agirligi / 7.0) * vke_bonusu)

if st.button("🚀 Raporu Oluştur ve Kaydet"):
    if surucu_adi:
        veriyi_kaydet(surucu_adi, puan, 0, 0, vke)
        st.balloons()
        
        # SERTİFİKA (Görseldeki Gibi)
        tarih_saat_kod = datetime.now().strftime("%d%m%y-%H%M")
        st.markdown(f"""
        <div style="border: 5px solid #F35C5C; border-radius: 15px; background-color: white; padding: 20px; max-width: 450px; margin: auto; text-align: center;">
            <h1 style="color: #F35C5C;">ERKOZ SERTİFİKASI</h1>
            <p><b>Sürücü:</b> {surucu_adi} | <b>Lisans:</b> 6012EXTREM-{tarih_saat_kod}</p>
            <div style="background-color: #38761D; color: white; padding: 20px; border-radius: 10px;">
                <h2>PUAN: {puan}</h2>
            </div>
            <p style="font-size: 11px; margin-top: 10px;">Düzenleme: {datetime.now().strftime('%d.%m.%Y')}</p>
        </div>
        """, unsafe_allow_html=True)

# LİG TABLOSU
st.markdown("---")
st.header("🏆 Şampiyonlar Ligi")
df_liste = veriyi_oku()
if not df_liste.empty:
    st.table(df_liste.sort_values(by="Puan", ascending=False).head(10))