import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner", layout="centered")

# --- TASARIM GÜNCELLEMESİ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Ödül ve Soru Bilgisi Paneli */
    .reward-banner {
        background-color: #f8f9fa; padding: 15px; border-radius: 12px;
        border: 2px solid #ffd700; text-align: center; margin-bottom: 20px;
        color: #11114e; font-weight: bold; font-size: 20px;
    }

    /* Soru Kutusu */
    .question-box {
        background: linear-gradient(145deg, #11114e, #1e1e8e);
        padding: 30px; border-radius: 20px; color: white;
        text-align: center; font-size: 22px; font-weight: bold;
        margin-bottom: 30px; min-height: 150px; display: flex;
        align-items: center; justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* 2x2 BUTON DÜZENİ */
    div[data-testid="stHorizontalBlock"] {
        gap: 15px !important;
    }

    /* Butonların Kendisi - Sabit Ölçü ve Şık Görünüm */
    .stButton>button {
        width: 100% !important;
        height: 70px !important; /* Yükseklik sabitlendi */
        border-radius: 15px !important;
        background: #2a2a61 !important;
        color: #ffd700 !important;
        border: 2px solid #5d5dff !important;
        font-weight: bold !important;
        font-size: 18px !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: #ffd700 !important;
        color: #11114e !important;
        border-color: #ffd700 !important;
        transform: scale(1.02);
    }

    /* Joker Bölümü */
    .joker-area {
        margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SORU HAVUZU ---
@st.cache_data
def get_tum_sorular():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası"},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman"},
        {"s": "İstiklal Marşı'mızın şairi kimdir?", "o": ["Ziya Gökalp", "Namık Kemal", "Mehmet Akif Ersoy", "Reşat Nuri"], "c": "Mehmet Akif Ersoy"},
        {"s": "Türkiye'nin yüzölçümü en büyük ili hangisidir?", "o": ["İstanbul", "Ankara", "Konya", "Erzurum"], "c": "Konya"},
        {"s": "Hangi gezegen 'Kızıl Gezegen' olarak bilinir?", "o": ["Venüs", "Mars", "Jüpiter", "Satürn"], "c": "Mars"},
        {"s": "Basketbolda bir periyot kaç dakikadır?", "o": ["8", "10", "12", "15"], "c": "10"},
        {"s": "Mona Lisa tablosu hangi müzede sergilenmektedir?", "o": ["Prado", "British Museum", "Louvre", "Hermitage"], "c": "Louvre"},
        {"s": "Dünya Kupası'nı en çok kazanan ülke hangisidir?", "o": ["Almanya", "İtalya", "Brezilya", "Arjantin"], "c": "Brezilya"},
        {"s": "Hangi hayvanın sütü pembe renklidir?", "o": ["Zürafa", "Su Aygırı", "Fil", "Gergedan"], "c": "Su Aygırı"},
        {"s": "Eyfel Kulesi hangi şehirdedir?", "o": ["Berlin", "Roma", "Paris", "Londra"], "c": "Paris"},
        {"s": "Osmanlı Devleti'nin kurucusu kimdir?", "o": ["Orhan Bey", "Osman Bey", "I. Murat", "Fatih Sultan Mehmet"], "c": "Osman Bey"},
        {"s": "Satrançta 'L' şeklinde hareket eden taş hangisidir?", "o": ["Fil", "Kale", "At", "Vezir"], "c": "At"}
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# --- OYUN DURUMU ---
if 'secili_sorular' not in st.session_state:
    havuz = get_tum_sorular()
    st.session_state.secili_sorular = random.sample(havuz, 12)
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.joker_erdal = True
    st.session_state.gizli_siklar = []

# --- ARAYÜZ ---
st.markdown('<h1 style="text-align:center; color:#11114e; margin-bottom:0;">💰 Milyoner</h1>', unsafe_allow_html=True)

if not st.session_state.elendi and st.session_state.index < 12:
    soru = st.session_state.secili_sorular[st.session_state.index]
    mevcut_odul = oduller[st.session_state.index]
    
    st.markdown(f'<div class="reward-banner">🏆 Soru: {st.session_state.index + 1}/12 | Ödül: {mevcut_odul}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # CEVAP BUTONLARI - TAM 2x2 DÜZEN
    col1, col2 = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        with (col1 if i % 2 == 0 else col2):
            if opt in st.session_state.gizli_siklar:
                st.button(" ", disabled=True, key=f"b_{i}_{st.session_state.index}")
            else:
                if st.button(opt, key=f"b_{i}_{st.session_state.index}"):
                    if opt == soru["c"]:
                        st.success("DOĞRU!")
                        time.sleep(1)
                        st.session_state.index += 1
                        st.session_state.gizli_siklar = []
                        st.rerun()
                    else:
                        st.session_state.elendi = True
                        st.rerun()

    # JOKERLER
    st.markdown('<div class="joker-area"></div>', unsafe_allow_html=True)
    j_col1, j_col2 = st.columns(2)
    with j_col1:
        if st.session_state.joker_50:
            if st.button("🃏 %50 Joker"):
                yanlislar = [o for o in soru['o'] if o != soru['c']]
                st.session_state.gizli_siklar = random.sample(yanlislar, 2)
                st.session_state.joker_50 = False
                st.rerun()
    with j_col2:
        if st.session_state.joker_erdal:
            if st.button("🤝 Erdal Kanki"):
                st.info(f"Erdal Kanki diyor ki: Doğru cevap '{soru['c']}'!")
                time.sleep(2)
                st.session_state.index += 1
                st.session_state.joker_erdal = False
                st.session_state.gizli_siklar = []
                st.rerun()

elif st.session_state.elendi:
    st.error(f"Yanlış Cevap! Kazancınız: {oduller[st.session_state.index-1] if st.session_state.index > 0 else '0 TL'}")
    if st.button("🔄 Yeniden Başla"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    st.balloons()
    st.success("🎉 TEBRİKLER! 1 MİLYON TL KAZANDINIZ!")
    if st.button("🎮 Yeniden Oyna"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
