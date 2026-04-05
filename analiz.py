import streamlit as st
import requests
import json
import urllib.parse
from datetime import date
from streamlit_local_storage import LocalStorage
# --- 0. STRAVA OAUTH AYARLARI (KRİTİK) ---
CLIENT_ID = "220679"
CLIENT_SECRET = "2107cf260184300e00123e266d7447c104fbf409" 
REDIRECT_URI = 'https://erdalkozalyazilim.streamlit.app'

# --- 1. KONFİGÜRASYON VE HAFIZA ---
st.set_page_config(page_title="Erkoz Analiz v48.7", layout="wide", page_icon="🚴‍♂️")

# --- 2. GİRİŞ KONTROLÜ VE OTOMATİK VERİ ÇEKME ---
query_params = st.query_params

if "code" not in query_params:
    st.title("🚀 Erkoz Performans Analiz v49.0")
    st.subheader("Hoş geldin! Devam etmek için Strava hesabınla bağlanman gerekiyor.")
    
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "read,activity:read_all",
        "approval_prompt": "auto"
    }
    auth_url = "https://www.strava.com/oauth/authorize?" + urllib.parse.urlencode(params)
    
    st.divider()
    st.link_button("🧡 Strava ile Giriş Yap", auth_url, type="primary")
    st.info("Bu giriş sayesinde sadece senin kendi verilerine erişebileceğiz.")
    st.stop() 
else:
    # 🎯 STRAVA'DAN VERİ ÇEKME MOTORU (KALORİ GÜNCELLEMELİ)
    if 'strava_data_fetched' not in st.session_state:
        try:
            code = query_params["code"]
            # Token alımı
            token_res = requests.post("https://www.strava.com/oauth/token", data={
                "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                "code": code, "grant_type": "authorization_code"
            }).json()

            if "access_token" in token_res:
                acc_token = token_res["access_token"]
                # Son 5 aktiviteyi çek
                act_res = requests.get(
                    "https://www.strava.com/api/v3/athlete/activities",
                    headers={"Authorization": f"Bearer {acc_token}"},
                    params={"per_page": 5}
                ).json()

                if act_res and isinstance(act_res, list):
                    last_act = act_res[0]
                    # Mesafe ve Yükselti
                    st.session_state['strava_km'] = round(last_act["distance"] / 1000, 2)
                    st.session_state['strava_yukselti'] = int(last_act.get("total_elevation_gain", 0))
                    
                    # 🔥 KALORİ HESABI (GÜNCELLENDİ)
                    # Önce direkt 'calories' verisine bakıyoruz
                    strava_cal = last_act.get("calories", 0)
                    # Eğer 0 gelirse 'kilojoules' üzerinden çeviri yapıyoruz
                    if strava_cal == 0:
                        strava_cal = int(last_act.get("kilojoules", 0) * 0.239)
                    
                    st.session_state['strava_kalori'] = strava_cal
                    st.session_state['strava_data_fetched'] = True
                    st.toast(f"✅ {last_act['type']} verileri ve {strava_cal} kcal başarıyla çekildi!")
        except Exception as e:
            st.error(f"Strava verisi çekilirken hata oluştu kanka.")

# --- 3. YEREL HAFIZA VE AYARLAR ---
local_storage = LocalStorage()
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

saved_user = local_storage.getItem("erkoz_user_data")
if 'user_data' not in st.session_state:
    if saved_user:
        st.session_state['user_data'] = json.loads(saved_user)
    else:
        st.session_state['user_data'] = {
            "ad_soyad": "İsim Soyisim", "dogum_tarihi": "1985-01-01", 
            "boy": 175, "kilo": 75.0, "bis_marka": "Model Girilmedi", "bis_kilosu": 10.0
        }

if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# --- 4. SOL PANEL (PROFİL) ---
with st.sidebar:
    st.header("⚙️ Sürücü Profili")
    u_ad = st.text_input("Ad Soyad", value=st.session_state['user_data']["ad_soyad"])
    #u_dt = st.date_input("Doğum Tarihi", value=date.fromisoformat(st.session_state['user_data']["dogum_tarihi"]))
    # 📅 TARİH SINIRI KALDIRILDI (1920 - 2026 Arası Serbest)
    u_dt = st.date_input(
        "Doğum Tarihi", 
        value=date(1967, 1, 1), # Varsayılan olarak seni 1967 yaptı kanka!
        min_value=date(1920, 1, 1), 
        max_value=date.today()
    )
    u_boy = st.number_input("Boy (cm)", value=int(st.session_state['user_data']["boy"]))
    u_kilo = st.number_input("Kilo (kg)", value=float(st.session_state['user_data']["kilo"]))
    st.markdown("---")
    u_bis = st.text_input("Bisiklet Modeli", value=st.session_state['user_data']["bis_marka"])
    u_biskilo = st.number_input("Donanım Ağırlığı (kg)", value=float(st.session_state['user_data']["bis_kilosu"]))

    if st.button("💾 BİLGİLERİMİ BU CİHAZA SABİTLE"):
        user_info = {"ad_soyad": u_ad, "dogum_tarihi": str(u_dt), "boy": u_boy, "kilo": u_kilo, "bis_marka": u_bis, "bis_kilosu": u_biskilo}
        local_storage.setItem("erkoz_user_data", json.dumps(user_info))
        st.session_state['user_data'] = user_info
        st.success("✅ Cihaza mühürlendi!")

    vke = round(u_kilo / ((u_boy/100)**2), 1)
    zorluk = round((u_biskilo - 10) * 2, 1)
    st.sidebar.metric("Anlık VKE", vke)
    st.sidebar.metric("Zorluk Katsayısı", f"%{zorluk}")

# --- 5. ANA EKRAN (GİRİŞ) ---
st.title(f"🚀 Erkoz Performans Analiz")
st.subheader(f"Hoş Geldin Erdal Abi")

# Hafızadan Strava verilerini alıyoruz
st_km = st.session_state.get('strava_km', 0.0)
st_yuk = st.session_state.get('strava_yukselti', 0)
st_kal = st.session_state.get('strava_kalori', 0)

col1, col2 = st.columns(2)
with col1:
    # Değerleri 'value' içine koyuyoruz ki kullanıcı değiştirebilsin
    km_in = st.number_input("Sürüş Mesafesi (KM)", value=float(st_km), step=0.01, format="%.2f")
    ruz_in = st.number_input("Ortalama Rüzgar (km/h)", value=0.0)
with col2:
    yuk_in = st.number_input("Toplam Yükselti (m)", value=int(st_yuk))
    # EĞER KALORİ 0 GELİRSE, BURAYA ELLE 499 YAZABİLECEKSİN
    kal_in = st.number_input("Yakılan Kalori (kcal)", value=int(st_kal))

# Bilgilendirme mesajı (Sadece kalori 0 ise çıkar)
if st_kal == 0 and st.session_state.get('strava_data_fetched'):
    st.info("ℹ️ Strava kalori verisini API üzerinden göndermedi. Web sitesinde gördüğün değeri yukarıya manuel yazabilirsin kanka.")

# --- 6. ANALİZ VE EXCEL ---
if st.button("📊 ANALİZİ TAMAMLA VE EXCEL'E UÇUR"):
    if km_in <= 0:
        st.error("KM girmeden analiz yapamayız!")
    elif km_in == st.session_state['last_km']:
        st.warning(f"⚠️ Bu veri zaten gönderildi!")
    else:
        yas = date.today().year - u_dt.year
        bak = 1 + (zorluk / 100)
        puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
        yag_gr = round((kal_in * 0.8) / 9, 1) if kal_in > 0 else 0

        payload = {
            "adSoyad": u_ad, "bisikleti": u_bis, "bisKilosu": u_biskilo,
            "surusTarihi": str(date.today()), "surusKM": km_in,
            "ruzgarHizi": ruz_in, "yukselti": yuk_in, "puan": puan
        }
        
        try:
            res = requests.post(SCRIPT_URL, json=payload, timeout=10)
            if res.status_code == 200:
                st.success(f"✅ Excel Senkronize Edildi! Puan: {puan}")
                st.session_state['last_km'] = km_in
                st.balloons()
                
                st.divider()
                with st.container(border=True):
                    st.header(f"🏆 BAŞARI SERTİFİKASI: {u_ad}")
                    st.write(f"🚲 {u_bis} | 👤 Yaş: {yas} | 👤 VKE: {vke}")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Mesafe", f"{km_in} KM")
                    m2.metric("Puan", puan)
                    m3.metric("Yükselti", f"{yuk_in} m")
                    m4.metric("Yağ Yakımı", f"{yag_gr} gr")
            else:
                st.error("❌ Sunucu hatası!")
        except:
            st.error("❌ Excel bağlantı hatası!")

st.caption("Erkoz Yazılım © 2026 | v49.0 - Turbo Mode")
