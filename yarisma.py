import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- GELİŞMİŞ MOBİL VE GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Ödül Bandı (Sorunun Üstünde Her Zaman Görünür) */
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

    /* Soru Kutusu */
    .question-box {
        background: linear-gradient(145deg, #11114e, #1e1e8e);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* --- 2x2 BUTON SİHRİ --- */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 12px !important;
    }
    
    div[data-testid="column"] {
        width: calc(50% - 15px) !important;
        flex: 0 0 calc(50% - 15px) !important;
        min-width: calc(50% - 15px) !important;
    }

    /* Cevap Butonları */
    .stButton>button {
        width: 100% !important;
        border-radius: 50px !important;
        height: 4em !important;
        background: #2a2a61 !important;
        color: #ffd700 !important;
        border: 2px solid #5d5dff !important;
        font-weight: bold !important;
        font-size: 15px !important;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background: #ffd700 !important;
        color: #11114e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SORU BANKASI ---
def get_soru_bankasi():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası", "z": 1},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman", "z": 1},
        {"s": "Türkiye'nin yüzölçümü en büyük ili hangisidir?", "o": ["İstanbul", "Ankara", "Konya", "Erzurum"], "c": "Konya", "z": 1}
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# Oyun Durumu
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.gizli_siklar = []
    st.session_state.secili_sorular = get_soru_bankasi()

# --- ARAYÜZ ---
st.markdown('<h2 style="text-align:center; color:#11114e;">💰 Milyoner</h2>', unsafe_allow_html=True)

if not st.session_state.elendi and st.session_state.index < len(st.session_state.secili_sorular):
    soru = st.session_state.secili_sorular[st.session_state.index]
    mevcut_odul = oduller[st.session_state.index]
    
    # 1. ÖDÜL LİSTESİ (YATAY BAND)
    st.markdown(f'<div class="reward-banner">🏆 Şu anki Ödül: {mevcut_odul}</div>', unsafe_allow_html=True)

    # 2. SORU KUTUSU
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # 3. 2x2 CEVAP BUTONLARI
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

    # Joker
    if st.session_state.joker_50:
        st.write("")
        if st.button("🃏 %50 Joker"):
            yanlislar = [o for o in soru['o'] if o != soru['c']]
            st.session_state.gizli_siklar = random.sample(yanlislar, 2)
            st.session_state.joker_50 = False
            st.rerun()

elif st.session_state.elendi:
    st.error("Kaybettiniz!")
    if st.button("Tekrar Dene"):
        st.session_state.clear()
        st.rerun()
else:
    st.balloons()
    st.success("1 MİLYON TL KAZANDINIZ!")
    if st.button("Yeniden Başla"):
        st.session_state.clear()
        st.rerun()
