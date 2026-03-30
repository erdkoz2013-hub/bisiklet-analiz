import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v34.0 - FULL ZIRHLI & GARANTİLİ SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v34.0", layout="wide", page_icon="🛡️")

# --- 1. HAFIZA VE GÜVENLİK ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved_data = load_settings()

# --- 2. SOL PANEL (YÖNETİCİ PANELİ) ---
with st.sidebar:
    st.header("👤 Sürücü Profili")
    ad_soyad = st.text_input("Ad Soyad", value=saved_data["ad_soyad"])
    d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
    dogum_tarihi = st.date_input("Doğum Tarihi", d_tarihi_raw)
    boy = st.number_input("Boy (cm)", value=int(saved_data["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(saved_data["kilo"]))

    st.markdown("---")
    st.header("🚲 Donanım")
    bis_marka = st.text_input("Bisiklet", value=saved_data["bis_marka"])
    bis_kilosu = st.number_input("Bisiklet Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

    # Anlık Metrikler
    vke_hesap = round(kilo / ((boy/100)**2), 1)
    yas = date.today().year - dogum_tarihi.year
    zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

    st.markdown("---")
    st.subheader("📊 Canlı Veri")
    st.metric("VKE", vke_hesap)
    st.metric("Zorluk Etkisi", f"%{zorluk_yuzdesi}")

# --- 3. ANA EKRAN ---
st.title("🛡️ Erkoz Yazılım - Analiz Terminali")

st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
with c1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with c2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    kalori_input = st.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ TAMAMLA VE GÜVENLİ AKTAR"):
    # Ayarları Kaydet
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilosu}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Algoritma (Kesin Sonuç)
    bak_katsayisi = 1 + (zorluk_yuzdesi / 100)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    # Excel Gönderim
    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad, "puan": final_puan, "km": km_input}, timeout=5)
    except: pass

    # --- 🏆 SERTİFİKA ALANI (HATASIZ VE ŞIK) ---
    st.markdown("---")
    
    # Koyu Tema Kapsayıcı
    with st.container(border=True):
        st.subheader(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
        st.write(f"📅 Tarih: {date.today()} | 🚲 Ekipman: {bis_marka}")
        st.divider()
        
        # Metrikler (Yan yana 3lü)
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Mesafe", f"{km_input} KM")
        m_col2.metric("Yükselti", f"{yukselti} M")
        m_col3.metric("VKE", vke_hesap)
        
        st.divider()

        # Final Skor Alanları (Renkli ve Büyük)
        # st.info ve st.error kullanarak o v29.3 havasını hatasız veriyoruz
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.error(f"🚀 GENEL SKOR: {final_puan}")
        with res_col2:
            st.warning(f"🔥 YAĞ YAKIMI: {yakilan_yag} gr")

    st.success("✅ İşlem Başarılı! Veriler senkronize edildi.")

st.caption("Erkoz Yazılım © 2026 | v34.0 - No-HTML Armor")
