import streamlit as st

# Sayfa Başlığı ve Tasarımı
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴")

st.title("🚴 Erkoz Hakkaniyetli Bisiklet Analiz")
st.subheader("Gerçek Sporcu Emeği Ölçüm Sistemi")

# --- 1. KİŞİSEL BİLGİLER VE HAVA ATMA HANESİ ---
st.sidebar.header("📋 Sürücü ve Ekipman Bilgileri")
surucu_adi = st.sidebar.text_input("Sürücü Adı Soyadı", "Ahmet Tatar")
bisiklet_marka = st.sidebar.text_input("Bisiklet Marka / Model", "Salcano XRS001")

# --- 2. TEKNİK VERİ GİRİŞLERİ ---
col1, col2 = st.columns(2)

with col1:
    yas = st.number_input("Yaşınız", min_value=10, max_value=100, value=45)
    kilo = st.number_input("Kilonuz (kg)", min_value=30.0, max_value=200.0, value=80.0)
    boy = st.number_input("Boyunuz (m)", min_value=1.0, max_value=2.5, value=1.75)

with col2:
    haftalik_km = st.number_input("Haftalık KM", min_value=0, value=150)
    haftalik_irtifa = st.number_input("Haftalık İrtifa (Metre)", min_value=0, value=500)
    # Senin 12 kg'lık makine ile 7 kg'lık Scott arasındaki farkı ölçecek sürgü
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 10.0)

ruzgar_pozisyonu = st.selectbox(
    "Grup İçindeki Pozisyon / Rüzgar",
    ["Kahraman (En Önde Rüzgarı Göğüsleyen)", "Takipçi (Rüzgar Arkası)", "Solo Sürüş"]
)

# --- 3. ERKOZ HAKKANİYET ALGORİTMASI ---
# Temel mantık: Aynı işi daha ağır bisikletle yapan daha başarılıdır!
standart_hafif_bisiklet = 7.0  # Referans ağırlık (Senin Scott Addict gibi)
agirlik_katsayisi = bisiklet_agirligi / standart_agirlik  # Ağırlaştıkça puan çarpanı artar

# Rüzgar Kahramanı Bonusu
ruzgar_bonusu = 1.30 if "Kahraman" in ruzgar_pozisyonu else 1.0

# Yaş Tecrübe Bonusu (60 yaşın adaleti!)
yas_bonusu = 1.0 + (yas / 100) 

# Başarı Puanı Hesaplama
# (Haftalık efor * Bisiklet Ağırlık Avantajı * Rüzgar Bonusu * Yaş Bonusu)
temel_efor = (haftalik_km * 0.5) + (haftalik_irtifa * 0.1)
final_skor = temel_efor * agirlik_katsayisi * ruzgar_bonusu * yas_bonusu

# --- 4. ŞIK RAPOR ÇIKTISI (PAYLAŞILABİLİR FORMAT) ---
if st.button("Hakkaniyetli Raporu Oluştur"):
    st.markdown("---")
    st.balloons() # Başarı kutlaması!
    
    # Rapor Tasarımı
    st.markdown(f"""
    <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
        <h2 style="text-align: center; color: #ff4b4b;">🏆 ERKOZ PERFORMANS SERTİFİKASI</h2>
        <p style="font-size: 18px;"><b>Sürücü:</b> {surucu_adi}</p>
        <p style="font-size: 18px;"><b>Ekipman:</b> {bisiklet_marka} (<span style="color:red;">{bisiklet_agirligi} kg</span>)</p>
        <hr>
        <p style="font-size: 16px;">Bu analiz, ekipman dezavantajı ve çevresel faktörler dikkate alınarak 
        <b>Erkoz Hakkaniyet Algoritması</b> ile hesaplanmıştır.</p>
        
        <h3 style="text-align: center;">BAŞARI PUANI: <span style="font-size: 40px; color: #2e7d32;">{int(final_skor)}</span></h3>
        
        <p style="text-align: right; font-style: italic;">"Hafif bisikletle herkes gider, asıl başarı ağırla rüzgarı yarmaktır."</p>
        <p style="text-align: right; font-weight: bold;">- Erkoz Yazılım 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Bu raporun ekran görüntüsünü alıp arkadaşına gönderebilirsin!")