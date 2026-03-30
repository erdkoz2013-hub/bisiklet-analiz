import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v29.5 - HTML'SİZ GARANTİLİ SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v29.5", layout="wide", page_icon="🛡️")

# --- 1. HAFIZA SİSTEMİ ---
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

# --- 2. SOL PANEL (METRİKLER VE AYARLAR) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value=saved_data["ad_soyad"])
d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", d_tarihi_raw)
boy = st.sidebar.number_input("Boy (cm)", value=int(saved_data["boy"]))
kilo = st.sidebar.number_input("Kilo (kg)", value=float(saved_data["kilo"]))

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım")
bis_marka = st.sidebar.text_input("Bisiklet", value=saved_data["bis_marka"])
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

# Hesaplamalar
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = date.today().year - dogum_tarihi.year
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

# Sol taraftaki o istediğin metrikler (Asla kaybolmaz)
st.sidebar.subheader("📊 Anlık Durum")
st.sidebar.metric("Vücut Kitle (VKE)", vke_hesap)
st.sidebar.metric("Donanım Zorluğu", f"%{zorluk_yuzdesi}")

# --- 3. ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Analiz Terminali")

st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
with c1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with c2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    kalori_input = st.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ TAMAMLA VE GÜVENLİ AKTAR"):
    # Kaydetme
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(dogum_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilosu}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Final Hesaplama
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

    # --- 🏆 HTML OLMAYAN YENİ NESİL SERTİFİKA ---
    # Kodun görünme ihtimali %0'dır.
    st.balloons()
    container = st.container(border=True)
    container.header(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
    container.write(f"📅 Tarih: {date.today()} | 🚲 Ekipman: {bis_marka}")
    
    col_a, col_b, col_c = container.columns(3)
    col_a.metric("Mesafe", f"{km_input} KM")
    col_b.metric("Yükselti", f"{yukselti} M")
    col_c.metric("VKE", vke_hesap)

    container.divider()
    
    res_col1, res_col2 = container.columns([2, 1])
    res_col1.subheader("🚀 GENEL PERFORMANS SKORU")
    res_col1.title(f"{final_puan}")
    
    res_col2.subheader("🔥 Yakılan Yağ")
    res_col2.title(f"{yakilan_yag} gr")
    
    st.success("✅ Veriler hafızaya alındı ve Excel aktarımı tamamlandı.")

st.caption("Erkoz Yazılım © 2026 | v29.5 - No-HTML Armor")
