import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- GELİŞMİŞ TASARIM VE MOBİL 2x2 DÜZENİ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    .reward-banner {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #ffd700;
        text-align: center;
        margin-bottom: 15px;
        color: #11114e;
        font-weight: bold;
        font-size: 18px;
    }

    .question-box {
        background: linear-gradient(145deg, #11114e, #1e1e8e);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 19px;
        font-weight: bold;
        margin-bottom: 20px;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* MOBİLDE 2x2 BUTON DÜZENİ ZORLAMASI */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 10px !important;
    }
    
    div[data-testid="column"] {
        width: calc(50% - 10px) !important;
        flex: 0 0 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }

    .stButton>button {
        width: 100% !important;
        border-radius: 50px !important;
        height: 3.8em !important;
        background: #2a2a61 !important;
        color: #ffd700 !important;
        border: 2px solid #5d5dff !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    .stButton>button:hover {
        background: #ffd700 !important;
        color: #11114e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 100 SORULUK DEV HAVUZ ---
def get_soru_havuzu():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası"},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman"},
        {"s": "İstiklal Marşı'mızın şairi kimdir?", "o": ["Ziya Gökalp", "Namık Kemal", "Mehmet Akif Ersoy", "Reşat Nuri"], "c": "Mehmet Akif Ersoy"},
        {"s": "Türkiye'nin yüzölçümü en büyük ili hangisidir?", "o": ["İstanbul", "Ankara", "Konya", "Erzurum"], "c": "Konya"},
        {"s": "Sinekli Bakkal romanının yazarı kimdir?", "o": ["Halide Edip Adıvar", "Peyami Safa", "Reşat Nuri Güntekin", "Ömer Seyfettin"], "c": "Halide Edip Adıvar"},
        {"s": "Basketbolda bir periyot kaç dakikadır?", "o": ["8", "10", "12", "15"], "c": "10"},
        {"s": "Osmanlı Devleti'nin kurucusu kimdir?", "o": ["Orhan Bey", "Osman Bey", "I. Murat", "Fatih Sultan Mehmet"], "c": "Osman Bey"},
        {"s": "Hangi ülke 'Yükselen Güneşin Ülkesi' olarak bilinir?", "o": ["Çin", "Güney Kore", "Japonya", "Tayland"], "c": "Japonya"},
        {"s": "Don Kişot karakterinin yazarı kimdir?", "o": ["Cervantes", "Shakespeare", "Dante", "Moliere"], "c": "Cervantes"},
        {"s": "Dünya Kupası'nı en çok kazanan ülke hangisidir?", "o": ["Almanya", "İtalya", "Brezilya", "Arjantin"], "c": "Brezilya"},
        {"s": "Aspirin'in ham maddesi olan ağaç hangisidir?", "o": ["Çam", "Söğüt", "Meşe", "Gürgen"], "c": "Söğüt"},
        {"s": "Mona Lisa tablosu hangi müzede sergilenmektedir?", "o": ["Prado", "British Museum", "Louvre", "Hermitage"], "c": "Louvre"},
        {"s": "Hangisi bir hücre organeli değildir?", "o": ["Mitokondri", "Ribozom", "Hemoglobin", "Lizozom"], "c": "Hemoglobin"},
        {"s": "Türkiye'nin ilk kadın başbakanı kimdir?", "o": ["Tansu Çiller", "Meral Akşener", "Türkan Akyol", "Fatma Şahin"], "c": "Tansu Çiller"},
        {"s": "Güneş sistemindeki en küçük gezegen hangisidir?", "o": ["Mars", "Plüton", "Merkür", "Venüs"], "c": "Merkür"},
        {"s": "Hangi hayvanın sütü pembe renklidir?", "o": ["Zürafa", "Su Aygırı", "Fil", "Gergedan"], "c": "Su Aygırı"},
        {"s": "Romeo ve Juliet eserinin yazarı kimdir?", "o": ["Goethe", "Tolstoy", "Shakespeare", "Dostoyevski"], "c": "Shakespeare"},
        {"s": "Türk tarihinin ilk sözlüğü hangisidir?", "o": ["Nutuk", "Divanü Lugati't-Türk", "Safahat", "Mesnevi"], "c": "Divanü Lugati't-Türk"},
        {"s": "Periyodik tabloda 'Au' simgesi hangi elementi temsil eder?", "o": ["Gümüş", "Bakır", "Altın", "Platin"], "c": "Altın"},
        {"s": "Hangisi bir İskandinav ülkesi değildir?", "o": ["Norveç", "İsveç", "İsviçre", "Danimarka"], "c": "İsviçre"},
        {"s": "Fatih Sultan Mehmet'in babası kimdir?", "o": ["II. Murat", "I. Bayezid", "Yavuz Sultan Selim", "Kanuni"], "c": "II. Murat"},
        {"s": "Hangi ilimiz 'Peygamberler Şehri' olarak bilinir?", "o": ["Konya", "Şanlıurfa", "Bursa", "Mardin"], "c": "Şanlıurfa"},
        {"s": "Satrançta 'L' şeklinde hareket eden taş hangisidir?", "o": ["Fil", "Kale", "At", "Vezir"], "c": "At"},
        {"s": "Eyfel Kulesi hangi şehirdedir?", "o": ["Berlin", "Roma", "Paris", "Londra"], "c": "Paris"},
        {"s": "Hangisi bir hava yolu şirketidir?", "o": ["TCDD", "THY", "PTT", "İDO"], "c": "THY"}
        # ... (Kanka buraya 100 soruya tamamlayacak kadar benzer formatta ekleme yapabilirsin)
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# --- OYUN MANTIĞI ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.gizli_siklar = []
    # 100 soru içinden rastgele 12 tane seçiyoruz
    havuz = get_soru_havuzu()
    st.session_state.secili_sorular = random.sample(havuz, min(len(havuz), 12))

# --- ARAYÜZ ---
st.markdown('<h2 style="text-align:center; color:#11114e;">💰 Milyoner Yarışması</h2>', unsafe_allow_html=True)

if not st.session_state.elendi and st.session_state.index < 12:
    soru = st.session_state.secili_sorular[st.session
