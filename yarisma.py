import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- Gelişmiş Tasarım (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #02021e; }
    
    /* Ödül Merdiveni Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #05052d;
        border-right: 2px solid #5d5dff;
    }
    .money-item {
        padding: 5px 10px;
        border-radius: 10px;
        margin-bottom: 2px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 18px;
    }
    .current-step {
        background-color: #ffd700;
        color: #02021e !important;
        border: 2px solid white;
    }
    .passed-step {
        color: #55557f !important;
    }
    .upcoming-step {
        color: #ffffff !important;
    }

    /* Soru ve Butonlar */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background: linear-gradient(to right, #0d0d4b, #1e1e8e);
        color: #ffd700;
        border: 2px solid #5d5dff;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .question-box {
        background: linear-gradient(145deg, #0d0d35, #161665);
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #5d5dff;
        color: white;
        text-align: center;
        font-size: 22px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SORU BANKASI ---
def get_soru_bankasi():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası", "z": 1},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman", "z": 1},
        {"s": "İstiklal Marşı'mızın şairi kimdir?", "o": ["Ziya Gökalp", "Namık Kemal", "Mehmet Akif Ersoy", "Reşat Nuri"], "c": Mehmet Akif Ersoy", "z": 1},
        {"s": "Sinekli Bakkal romanının yazarı kimdir?", "o": ["Halide Edip Adıvar", "Peyami Safa", "Reşat Nuri Güntekin", "Ömer Seyfettin"], "c": "Halide Edip Adıvar", "z": 2},
        {"s": "Basketbolda bir periyot kaç dakikadır?", "o": ["8", "10", "12", "15"], "c": "10", "z": 2},
        {"s": "Osmanlı Devleti'nin kurucusu kimdir?", "o": ["Orhan Bey", "Osman Bey", "I. Murat", "Fatih Sultan Mehmet"], "c": "Osman Bey", "z": 3},
        {"s": "Hangi ülke 'Yükselen Güneşin Ülkesi' olarak bilinir?", "o": ["Çin", "Güney Kore", "Japonya", "Tayland"], "c": "Japonya", "z": 3},
        {"s": "Don Kişot karakterinin yazarı kimdir?", "o": ["Cervantes", "Shakespeare", "Dante", "Moliere"], "c": "Cervantes", "z": 4},
        {"s": "Dünya Kupası'nı en çok kazanan ülke hangisidir?", "o": ["Almanya", "İtalya", "Brezilya", "Arjantin"], "c": "Brezilya", "z": 4},
        {"s": "Aspirin'in ham maddesi olan ağaç hangisidir?", "o": ["Çam", "Söğüt", "Meşe", "Gürgen"], "c": "Söğüt", "z": 5},
        {"s": "Nobel ödülleri hangi ülkede verilmektedir?", "o": ["Norveç-İsveç", "Almanya", "ABD", "İngiltere"], "c": "Norveç-İsveç", "z": 6},
        {"s": "Mona Lisa tablosu hangi müzede sergilenmektedir?", "o": ["Prado", "British Museum", "Louvre", "Hermitage"], "c": "Louvre", "z": 7}
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# --- OYUN DURUMU ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.havuz = get_soru_bankasi()
    st.session_state.secili_sorular = []
    # Basit bir seçim mantığı: Her zorluktan veya sıradan sorular
    for i in range(len(oduller)):
        st.session_state.secili_sorular.append(st.session_state.havuz[i % len(st.session_state.havuz)])

if 'joker_50' not in st.session_state:
    st.session_state.joker_50 = True
    st.session_state.gizli_siklar = []

# --- ARAYÜZ ---
st.title("💰 Kim Milyoner Olmak İster?")

if not st.session_state.elendi and st.session_state.index < len(oduller):
    soru = st.session_state.secili_sorular[st.session_state.index]
    
    # Gelişmiş Ödül Merdiveni (Sidebar)
    st.sidebar.markdown("### 🏆 Ödül Tablosu")
    for i, o in enumerate(reversed(oduller)):
        idx = len(oduller) - 1 - i
        if idx == st.session_state.index:
            class_name = "current-step"
            label = "👉 " + o
        elif idx < st.session_state.index:
            class_name = "passed-step"
            label = "✅ " + o
        else:
            class_name = "upcoming-step"
            label = "▫️ " + o
        
        st.sidebar.markdown(f'<div class="money-item {class_name}">{label}</div>', unsafe_allow_html=True)

    # Jokerler Bölümü
    st.sidebar.markdown("---")
    st.sidebar.subheader("🃏 Jokerler")
    if st.session_state.joker_50:
        if st.sidebar.button("%50 Jokerini Kullan"):
            yanlislar = [opt for opt in soru['o'] if opt != soru['c']]
            st.session_state.gizli_siklar = random.sample(yanlislar, 2)
            st.session_state.joker_50 = False
            st.rerun()
    else:
        st.sidebar.write("❌ %50 Jokeri Kullanıldı")

    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        if opt in st.session_state.gizli_siklar:
            cols[i % 2].button(f" ", disabled=True, key=f"btn_{i}")
        else:
            with cols[i % 2]:
                if st.button(opt, key=f"btn_{i}"):
                    if opt == soru["c"]:
                        st.success("DOĞRU!")
                        time.sleep(1)
                        st.session_state.index += 1
                        st.session_state.gizli_siklar = []
                        st.rerun()
                    else:
                        st.error(f"YANLIŞ! Doğru cevap: {soru['c']}")
                        st.session_state.elendi = True
                        st.rerun()

elif st.session_state.elendi:
    st.error(f"Elendiniz! Kazancınız: {oduller[st.session_state.index-1] if st.session_state.index > 0 else '0 TL'}")
    if st.button("Tekrar Oyna"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.balloons()
    st.success("TEBRİKLER! 1 MİLYON TL'NİN SAHİBİ OLDUNUZ!")
    if st.button("Yeniden Başla"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
