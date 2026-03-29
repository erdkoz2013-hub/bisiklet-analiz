import streamlit as st

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴")

st.title("🚴 Erkoz Hakkaniyetli Bisiklet Analiz")
st.subheader("Gerçek Sporcu Emeği Ölçüm Sistemi")

# 2. Giriş Alanları
st.sidebar.header("📋 Sürücü ve Ekipman")
surucu_adi = st.sidebar.text_input("Sürücü Adı Soyadı", "Ahmet Tatar")
bisiklet_marka = st.sidebar.text_input("Bisiklet Marka / Model", "Salcano XRS001")

col1, col2 = st.columns(2)
with col1:
    yas = st.number_input("Yaşınız", min_value=10, max_value=100, value=60)
    kilo = st.number_input("Kilonuz (kg)", min_value=30.0, max_value=200.0, value=80.0)
    boy = st.number_input("Boyunuz (m)", min_value=1.0, max_value=2.5, value=1.75)
with col2:
    haftalik_km = st.number_input("Haftalık KM", min_value=0, value=150)
    haftalik_irtifa = st.number_input("Haftalık İrtifa (Metre)", min_value=0, value=1000)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 12.0)

ruzgar_pozisyonu = st.selectbox("Grup İçi Pozisyon", ["Kahraman (Önde)", "Takipçi", "Solo"])

# 3. Hesaplama (Erkoz Algoritması)
agirlik_katsayisi = bisiklet_agirligi / 7.0 
ruzgar_bonusu = 1.30 if "Kahraman" in ruzgar_pozisyonu else 1.0
yas_bonusu = 1.0 + (yas / 100) 
final_skor = int(((haftalik_km * 0.5) + (haftalik_irtifa * 0.1)) * agirlik_katsayisi * ruzgar_bonusu * yas_bonusu)

st.success(f"📊 Mevcut Hesaplanan Hakkaniyet Puanı: *{final_skor}*")

# 4. ŞIK RAPOR (HATASIZ YÖNTEM)
if st.button("Hakkaniyetli Raporu Oluştur"):
    st.balloons()
    
    # Rapor Başlığı
    st.markdown(f"""
    <div style="border: 4px solid #ff4b4b; padding: 20px; border-radius: 15px; background-color: #ffffff; text-align: center;">
        <h1 style="color: #ff4b4b; margin-bottom: 0;">🏆 ERKOZ PERFORMANS SERTİFİKASI</h1>
        <p style="color: gray;">Lisans No: {yas}{int(bisiklet_agirligi)}EXTREM</p>
        <hr style="border: 1px solid #eee;">
        <div style="text-align: left; font-size: 20px;">
            <p><b>Sürücü:</b> {surucu_adi}</p>
            <p><b>Ekipman:</b> {bisiklet_marka} ({bisiklet_agirligi} kg)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # BAŞARI PUANI (Ayrı bir kutu olarak, en güvenli şekilde)
    st.markdown(f"""
    <div style="background-color: #2e7d32; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 10px;">
        <p style="font-size: 20px; margin-bottom: 0;">HAKKANİYETLİ BAŞARI PUANI</p>
        <h1 style="font-size: 60px; margin-top: 0;">{final_skor}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Alt Bilgi
    st.markdown(f"""
    <div style="text-align: right; margin-top: 15px; font-style: italic;">
        <p>"Hafif bisikletle herkes gider, asıl başarı ağırla rüzgarı yarmaktır."</p>
        <p><b>- Erkoz Yazılım 2026</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Bu raporun ekran görüntüsünü alıp arkadaşlarına gönderebilirsin!")