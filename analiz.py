import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v22.0 - KESİN ÇÖZÜM
st.set_page_config(page_title="Erkoz Analiz v22.0", layout="wide", page_icon="🚴‍♂️")

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Analiz")
st.markdown("---")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- MOTOR ---
def ruzgar_kademesi_bul(hiz):
    if hiz <= 15: return 1
    elif hiz <= 30: return 2
    else: return 3

def hesapla_standart_puan(yas, haftalik_km, beslenme, vke_puani):
    return round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_puani, 3)

# --- ARAYÜZ ---
st.sidebar.header("👤 Kullanıcı Profili")
ad_soyad = st.sidebar.text_input("Sürücü Adı Soyadı", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

vke = round(kilo / ((boy/100)**2), 1)
vke_katkisi = round((vke / 100) * 20, 2)
st.sidebar.info(f"💡 VKE: {vke} | Katkı: +{vke_katkisi}")

bisiklet = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.number_input("Beslenme (1-3)", value=3)

yas = date.today().year - dogum_tarihi.year
std_puan = hesapla_standart_puan(yas, haftalik_km, beslenme, vke_katkisi)

col1, col2 = st.columns(2)
with col1:
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=100.0)
with col2:
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    yukselti = st.number_input("Yükselti (m)", value=1049)

if st.button("🚀 ANALİZİ TAMAMLA VE KAYDET"):
    # Hesaplamalar
    km_puani = round((std_puan / surus_km) * 100, 3)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani, 3)
    
    payload = {
        "adSoyad": ad_soyad, "dogumTarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo,
        "bisikletModeli": bisiklet, "bisikletKilosu": 15.0, "haftalikKM": haftalik_km,
        "beslenmeDuzeyi": beslenme, "surusTarihi": str(surus_tarihi), "surusKM": surus_km,
        "ruzgar": ruzgar_hizi, "yukselti": yukselti, "surusPuani": final_puan
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # --- TEKNİK DÜZELTME: HTML'İ DAHA GÜVENLİ YAZDIRIYORUZ ---
        cert_container = f"""
        <div style="background-color: #0E1117; border: 5px double #FF4B4B; padding: 20px; border-radius: 15px; font-family: sans-serif; color: white;">
            <h2 style="color: #FF4B4B; text-align: center; margin-top: 0;">🏆 ERKOZ PERFORMANS ANALİZİ</h2>
            <p style="text-align: center; color: #888;">Tarih: {surus_tarihi}</p>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td><small style="color:#888">Sürücü:</small><br><b>{ad_soyad}</b></td>
                    <td style="text-align:right"><small style="color:#888">Bisiklet:</small><br><b>{bisiklet}</b></td>
                </tr>
            </table>
            
            <hr style="border: 0.5px solid #333; margin: 15px 0;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Mesafe: {surus_km} KM</small><br><b style="color:#00D4FF">Temel: {km_puani}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Rüzgar: {ruzgar_hizi} km/h</small><br><b style="color:#00D4FF">Primi: +{ruzgar_katkisi}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">Yükselti: {yukselti} M</small><br><b style="color:#00D4FF">Primi: +{yukselti_puani}</b>
                </div>
                <div style="background:#161B22; padding:10px; border-radius:8px;">
                    <small style="color:#888">VKE Endeks: {vke}</small><br><b style="color:#00D4FF">Avantaj: +{vke_katkisi}</b>
                </div>
            </div>
            
            <div style="margin-top: 20px; background: #1F2937; padding: 15px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                <small style="color:#888; letter-spacing: 2px;">GENEL SÜRÜŞ SKORU</small>
                <h1 style="color: #FF4B4B; font-size: 50px; margin: 0;">{final_puan}</h1>
            </div>
            
            <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #333; display: flex; justify-content: space-between; align-items: center;">
                <b style="color: #FF4B4B; font-size: 14px;">Erkoz Yazılım Ar-Ge</b>
                <div style="text-align: right;">
                    <small style="color: #555;">Analiz Onay</small><br>
                    <span style="color: #EEE; font-size: 18px;"><i>Erdal Kozal</i></span>
                </div>
            </div>
        </div>
        """
        # "unsafe_allow_html=True" buradaki en kritik parça, bir harf bile şaşmamalı
        st.write("---")
        st.components.v1.html(cert_container, height=550, scrolling=False)
        st.success("Tebrikler kanka! Belgen pırıl pırıl hazır.")
    except:
        st.error("Bağlantı hatası.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Performans Analiz Merkezi")
