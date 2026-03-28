import streamlit as st

st.set_page_config(page_title="Erdal Kozal Analiz v2.7", layout="centered")

st.title("🚲 Erdal Kozal Başarı Analizörü v2.7")
st.sidebar.header("📊 Kullanıcı ve Sürüş Detayları")

# 1. Kişisel Bilgiler
yas = st.sidebar.number_input("Yaşınız", 15, 100, 45)
kilo = st.sidebar.number_input("Kilonuz (kg)", 40.0, 200.0, 80.0)
boy = st.sidebar.number_input("Boyunuz (Örn: 1.75)", 1.20, 2.20, 1.75)
vki = kilo / (boy * boy)

st.sidebar.write(f"*Hesaplanan VKİ:* {vki:.2f}")
st.sidebar.write("---")

# 2. Sürüş Bilgileri
km = st.sidebar.number_input("Haftalık KM", 0, 1000, 150)
irtifa = st.sidebar.number_input("Haftalık İrtifa (Metre)", 0, 5000, 500)
agirlik = st.sidebar.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 10.0)

# 3. Rüzgar ve Grup Pozisyonu (Yeni Kriter!)
pozisyon = st.sidebar.selectbox("Grup İçindeki Pozisyon / Rüzgar", 
                                ["Kahraman (En Önde Rüzgarı Göğüsleyen)", 
                                 "Tek Tabanca (Bireysel Sürüş)", 
                                 "Çakal (Grup Ortasında Siperde)"])

# 4. Beslenme
besin = st.sidebar.selectbox("Beslenme Düzeni", 
                             ["Düşük Kalorili / Fit", 
                              "Orta Kalorili / Dengeli", 
                              "Yüksek Kalorili / Karbonhidrat Odaklı"])

# --- HESAPLAMA MANTIĞI ---
p1 = ((yas + 20) / 100) * 3  # Yaş tecrübe puanı
p2 = 3.0 if 18.5 <= vki <= 25 else 2.0  # VKİ puanı
p3 = (km / 100) * 2.5  # Mesafe puanı
t_etki = (irtifa / 500) * 1.5  # İrtifa puanı

# Rüzgar Çarpanı (Senin istediğin o kritik dokunuş)
if "Kahraman" in pozisyon:
    r_puani = 3.5  # En yüksek efor!
elif "Tek Tabanca" in pozisyon:
    r_puani = 2.5  # Ciddi efor
else:
    r_puani = 1.0  # Rüzgar yemediği için düşük efor puanı

# Beslenme ve Bisiklet Ağırlığı
p5 = 3.0 if "Düşük" in besin else 2.0 if "Orta" in besin else 1.0
p6 = (20 - agirlik) / 5  # Bisiklet hafifledikçe puan artar

toplam_puan = p1 + p2 + p3 + t_etki + r_puani + p5 + p6

# --- EKRAN GÖSTERGESİ ---
c1, c2, c3 = st.columns(3)
c1.metric("🏆 BAŞARI PUANI", f"{toplam_puan:.2f}")
c2.metric("⛰️ İRTİFA ETKİSİ", f"+{t_etki:.2f}")
c3.metric("🌬️ RÜZGAR EFORU", f"+{r_puani:.2f}")

st.write("---")

# Kahve Masası Karşılaştırma Notu
if "Kahraman" in pozisyon:
    st.success("🔥 Helal olsun! Grubu sen taşıdın, rüzgarı sen yedin. Puanın hakkındır!")
elif "Çakal" in pozisyon:
    st.warning("🤫 Akıllıca! Rüzgardan kaçtın, enerjiyi sona sakladın. Ama puanın biraz düşük kaldı.")

def rapor_hazirla():
    return f"""
    ERDAL KOZAL ANALIZ RAPORU (v2.7)
    ---------------------------------
    Yas: {yas} | VKİ: {vki:.2f}
    Pozisyon: {pozisyon}
    Beslenme: {besin}
    ---------------------------------
    Haftalik KM: {km} | Irtifa: {irtifa}m
    ---------------------------------
    TOPLAM BASARI PUANI: {toplam_puan:.2f}
    """

st.download_button("📥 Raporu Al (.txt)", rapor_hazirla(), "analiz_v2.7.txt")
st.info("İzmir'in yollarında, rüzgarın hep arkanda olsun kankam!")