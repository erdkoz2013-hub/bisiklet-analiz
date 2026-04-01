import streamlit as st
import time
import random


# ==========================================
# ⚙️ SADECE BURADAKİ RAKAMLARI DEĞİŞTİR:
KUTU_YUKSEKLIGI = 50   # Kutuların dikine boyu (70, 80, 90 dene)
YAZI_BOYUTU = 16       # Cevapların yazı büyüklüğü (14 veya 18 dene)
ARALIK_BOSLUGU = 10    # Kutuların arasındaki mesafe (5 veya 15 dene)
# ==========================================

st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: {ARALIK_BOSLUGU}px !important;
    }}
    div[data-testid="column"] {{
        flex: 1 1 calc(50% - {ARALIK_BOSLUGU + 5}px) !important;
        min-width: calc(50% - {ARALIK_BOSLUGU + 5}px) !important;
    }}
    .stButton>button {{
        width: 100% !important;
        height: {KUTU_YUKSEKLIGI}px !important;
        font-size: {YAZI_BOYUTU}px !important;
        background: #2a2a61 !important;
        color: #ffd700 !important;
        border-radius: 12px !important;
        border: 2px solid #5d5dff !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# Sayfa ayarları
st.set_page_config(page_title="Milyoner", layout="centered")

# --- CSS: KUTULARI VE BUTONLARI DEMİR GİBİ SABİTLEME ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    .reward-banner {
        background-color: #f8f9fa; padding: 12px; border-radius: 10px;
        border: 2px solid #ffd700; text-align: center; margin-bottom: 15px;
        color: #11114e; font-weight: bold; font-size: 18px;
    }

    .question-box {
        background: linear-gradient(145deg, #11114e, #1e1e8e);
        padding: 25px; border-radius: 15px; color: white;
        text-align: center; font-size: 20px; font-weight: bold;
        margin-bottom: 25px; min-height: 140px; display: flex;
        align-items: center; justify-content: center;
    }

    /* KUTU BOYUTLARINI %50 GENİŞLİĞE KİLİTLER */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        width: 100% !important;
        gap: 10px !important;
    }


    .stButton>button:hover {
        background: #ffd700 !important;
        color: #11114e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GENİŞLETİLMİŞ SORU HAVUZU ---
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
        {"s": "Kabe hangi şehirdedir?", "o": ["Riyad", "Medine", "Mekke", "Cidde"], "c": "Mekke"},
        {"s": "Aspirin'in ham maddesi olan ağaç hangisidir?", "o": ["Çam", "Söğüt", "Meşe", "Gürgen"], "c": "Söğüt"},
        {"s": "Satrançta 'L' şeklinde hareket eden taş hangisidir?", "o": ["Fil", "Kale", "At", "Vezir"], "c": "At"},
        {"s": "Türkiye'nin ilk kadın başbakanı kimdir?", "o": ["Tansu Çiller", "Meral Akşener", "Türkan Akyol", "Fatma Şahin"], "c": "Tansu Çiller"},
        {"s": "Güneş sistemindeki en küçük gezegen hangisidir?", "o": ["Mars", "Plüton", "Merkür", "Venüs"], "c": "Merkür"},
        {"s": "Don Kişot karakterinin yazarı kimdir?", "o": ["Cervantes", "Shakespeare", "Dante", "Moliere"], "c": "Cervantes"},
        {"s": "Hangi ilimiz 'Peygamberler Şehri' olarak bilinir?", "o": ["Konya", "Şanlıurfa", "Bursa", "Mardin"], "c": "Şanlıurfa"},
        {"s": "Cumhuriyet kaç yılında ilan edilmiştir?", "o": ["1920", "1921", "1922", "1923"], "c": "1923"},
        {"s": "Türk Tarih Kurumu'nun ilk başkanı kimdir?", "o": ["Tevfik Bıyıklıoğlu", "Afet İnan", "Yusuf Akçura", "Reşit Galip"], "c": "Tevfik Bıyıklıoğlu"},
        {"s": "Hangisi bir hücre organeli değildir?", "o": ["Mitokondri", "Ribozom", "Hemoglobin", "Lizozom"], "c": "Hemoglobin"},
        {"s": "Nobel Edebiyat Ödülü'nü alan ilk Türk yazar kimdir?", "o": ["Yaşar Kemal", "Orhan Pamuk", "Aziz Nesin", "Elif Şafak"], "c": "Orhan Pamuk"},
        {"s": "Fatih Sultan Mehmet kaç yaşında İstanbul'u fethetmiştir?", "o": ["19", "21", "23", "25"], "c": "21"},
        {"s": "Yüz ölçümü bakımından dünyanın en büyük ülkesi hangisidir?", "o": ["ABD", "Çin", "Kanada", "Rusya"], "c": "Rusya"},
        {"s": "Hangisi Kanuni Sultan Süleyman'ın lakabıdır?", "o": ["Yavuz", "Muhteşem", "Fatih", "Yıldırım"], "c": "Muhteşem"},
        {"s": "Akdeniz ile Kızıldeniz'i birbirine bağlayan kanal hangisidir?", "o": ["Panama", "Süveyş", "Korint", "Kiel"], "c": "Süveyş"},
        {"s": "Telefonun mucidi kimdir?", "o": ["Edison", "Tesla", "Graham Bell", "Marconi"], "c": "Graham Bell"},
        {"s": "Türkiye'nin en uzun nehri hangisidir?", "o": ["Fırat", "Dicle", "Kızılırmak", "Sakarya"], "c": "Kızılırmak"},
        {"s": "Yedi Renkli Göl olarak bilinen gölümüz hangisidir?", "o": ["Van Gölü", "Eğirdir Gölü", "Beyşehir Gölü", "Tuz Gölü"], "c": "Eğirdir Gölü"},
        {"s": "Türk parasından 6 sıfır kaç yılında atılmıştır?", "o": ["2003", "2004", "2005", "2006"], "c": "2005"},
        {"s": "Hangi gezegen Güneş sistemindeki en sıcak gezegendir?", "o": ["Merkür", "Venüs", "Mars", "Jüpiter"], "c": "Venüs"},
        {"s": "Modern hemşireliğin kurucusu kabul edilen kişi kimdir?", "o": ["Marie Curie", "Florence Nightingale", "Rosa Parks", "Ada Lovelace"], "c": "Florence Nightingale"},
        {"s": "Dünyanın en yüksek şelalesi hangisidir?", "o": ["Niagara", "Victoria", "Angel", "Iguazu"], "c": "Angel"},
        {"s": "Periyodik tabloda 'Fe' simgesi hangi elementi temsil eder?", "o": ["Bakır", "Altın", "Demir", "Flor"], "c": "Demir"},
        {"s": "Hangi ünlü ressam kendi kulağını kesmiştir?", "o": ["Picasso", "Salvador Dali", "Vincent van Gogh", "Claude Monet"], "c": "Vincent van Gogh"},
        {"s": "Sefiller (Les Misérables) romanının yazarı kimdir?", "o": ["Victor Hugo", "Balzac", "Emile Zola", "Gustave Flaubert"], "c": "Victor Hugo"},
        {"s": "Olimpiyat halkalarında hangi renk yoktur?", "o": ["Mavi", "Sarı", "Turuncu", "Yeşil"], "c": "Turuncu"},
        {"s": "Dünyanın en küçük kıtası hangisidir?", "o": ["Avrupa", "Antarktika", "Avustralya", "Güney Amerika"], "c": "Avustralya"},
        {"s": "Satrançta en güçlü taş hangisidir?", "o": ["Şah", "Kale", "Fil", "Vezir"], "c": "Vezir"},
        {"s": "Hangi ülkenin üç tane başkenti vardır?", "o": ["İsviçre", "Güney Afrika", "Kanada", "Avustralya"], "c": "Güney Afrika"},
        {"s": "İnsan vücudundaki en küçük kemik nerededir?", "o": ["Burun", "El", "Kulak", "Ayak"], "c": "Kulak"},
        {"s": "Kıbrıs Barış Harekatı hangi yıl gerçekleşmiştir?", "o": ["1963", "1967", "1974", "1980"], "c": "1974"},
        {"s": "Hangi Türk devleti tarihte ilk kez yerleşik hayata geçmiştir?", "o": ["Hunlar", "Göktürkler", "Uygurlar", "Hazarlar"], "c": "Uygurlar"},
        {"s": "Mona Lisa tablosu hangi tür ahşap üzerine resmedilmiştir?", "o": ["Meşe", "Kavak", "Çam", "Gürgen"], "c": "Kavak"},
        {"s": "Türkiye'nin en kuzey noktası olan ilimiz hangisidir?", "o": ["Kırklareli", "Artvin", "Sinop", "Kastamonu"], "c": "Sinop"},
        {"s": "İnternetin atası sayılan ağın adı nedir?", "o": ["ARPANET", "ETHERNET", "INTRANET", "USENET"], "c": "ARPANET"},
        {"s": "Hangi hayvan su altında nefes alamaz?", "o": ["Köpekbalığı", "Balina", "Ahtapot", "Vatoz"], "c": "Balina"},
        {"s": "Eiffel Kulesi'nin mimarı kimdir?", "o": ["Gustave Eiffel", "Le Corbusier", "Frank Lloyd Wright", "Gaudi"], "c": "Gustave Eiffel"},
        {"s": "İlk Nobel Barış Ödülü'nü kazanan Kızılhaç kurucusu kimdir?", "o": ["Albert Schweitzer", "Henry Dunant", "Martin Luther King", "Nelson Mandela"], "c": "Henry Dunant"},
        {"s": "Hangi ülke 'Laleler Ülkesi' olarak anılır?", "o": ["Belçika", "Hollanda", "Fransa", "Danimarka"], "c": "Hollanda"},
        {"s": "Osmanlı'da 'Lale Devri' hangi padişah dönemindedir?", "o": ["III. Ahmet", "IV. Murat", "II. Mahmut", "Abdülmecit"], "c": "III. Ahmet"},
        {"s": "DNA'nın çift sarmallı yapısını keşfedenlerden biri kimdir?", "o": ["Newton", "Darwin", "James Watson", "Einstein"], "c": "James Watson"},
        {"s": "Hangi enstrüman 'enstrümanların kralı' olarak bilinir?", "o": ["Keman", "Piyano", "Arp", "Org"], "c": "Org"},
        {"s": "Dünyanın en yüksek binası Burç Halife hangi şehirdedir?", "o": ["Abu Dabi", "Riyad", "Dubai", "Kuveyt"], "c": "Dubai"},
        {"s": "İlk sesli sinema filmi hangisidir?", "o": ["The Jazz Singer", "Citizen Kane", "Casablanca", "Metropolis"], "c": "The Jazz Singer"},
        {"s": "Hangi ülke Güney Amerika kıtasında değildir?", "o": ["Peru", "Meksika", "Şili", "Kolombiya"], "c": "Meksika"},
        {"s": "Bilgisayar biliminin babası kabul edilen matematikçi kimdir?", "o": ["Alan Turing", "Bill Gates", "Steve Jobs", "Blaise Pascal"], "c": "Alan Turing"},
        {"s": "Hangi elementin atom numarası 1'dir?", "o": ["Helyum", "Oksijen", "Hidrojen", "Karbon"], "c": "Hidrojen"},
        {"s": "Süveyş Kanalı hangi iki denizi birbirine bağlar?", "o": ["Akdeniz - Karadeniz", "Akdeniz - Kızıldeniz", "Ege - Marmara", "Hazar - Karadeniz"], "c": "Akdeniz - Kızıldeniz"},
        {"s": "Hangi vitamin kanın pıhtılaşmasını sağlar?", "o": ["A Vitamini", "C Vitamini", "E Vitamini", "K Vitamini"], "c": "K Vitamini"},
        {"s": "Titanik gemisi hangi yıl batmıştır?", "o": ["1905", "1912", "1920", "1933"], "c": "1912"},
        {"s": "Hangi ülke Büyük Britanya adasında yer almaz?", "o": ["Galler", "İskoçya", "İrlanda Cumhuriyeti", "İngiltere"], "c": "İrlanda Cumhuriyeti"},
        {"s": "İlk matbaayı kim icat etmiştir?", "o": ["Edison", "Johannes Gutenberg", "James Watt", "Leonardo da Vinci"], "c": "Johannes Gutenberg"},
        {"s": "Hangi ilimizde Peri Bacaları bulunmaktadır?", "o": ["Kayseri", "Nevşehir", "Niğde", "Aksaray"], "c": "Nevşehir"},
        {"s": "Suç ve Ceza romanının baş karakteri kimdir?", "o": ["Jean Valjean", "Raskolnikov", "Oliver Twist", "Anna Karenina"], "c": "Raskolnikov"},
        {"s": "İstiklal Marşı'mızda 'milletimindir' kelimesi kaç kez geçer?", "o": ["1", "2", "3", "4"], "c": "1"},
        {"s": "Hangi gezegenin halkası en belirgindir?", "o": ["Jüpiter", "Satürn", "Uranüs", "Neptün"], "c": "Satürn"},
        {"s": "Dünyanın en geniş yüzölçümüne sahip ülkesi hangisidir?", "o": ["Kanada", "Çin", "Rusya", "ABD"], "c": "Rusya"},
        {"s": "Türkiye'nin en doğusundaki il hangisidir?", "o": ["Kars", "Iğdır", "Van", "Hakkari"], "c": "Iğdır"},
        {"s": "Hangi organımızda 'Langerhans Adacıkları' bulunur?", "o": ["Karaciğer", "Böbrek", "Pankreas", "Dalak"], "c": "Pankreas"},
        {"s": "Asya ve Avrupa'yı birbirine bağlayan ilk köprü hangisidir?", "o": ["Fatih Sultan Mehmet", "15 Temmuz Şehitler", "Yavuz Sultan Selim", "Osmangazi"], "c": "15 Temmuz Şehitler"},
        {"s": "Hangi meyvenin çekirdeği dışındadır?", "o": ["Böğürtlen", "Çilek", "Ahududu", "İncir"], "c": "Çilek"},
        {"s": "Sherlock Holmes karakterinin yaratıcısı kimdir?", "o": ["Agatha Christie", "Arthur Conan Doyle", "Edgar Allan Poe", "Stephen King"], "c": "Arthur Conan Doyle"},
        {"s": "Aşağıdaki dillerden hangisi Latin alfabesi kullanmaz?", "o": ["Almanca", "Fransızca", "Rusça", "İtalyanca"], "c": "Rusça"},
        {"s": "Hangi ilimizin adı 'Güzel Atlar Ülkesi' anlamına gelir?", "o": ["Konya", "Kapadokya (Nevşehir)", "Erzurum", "Mardin"], "c": "Kapadokya (Nevşehir)"},
        {"s": "Dünyanın en kalabalık ülkesi hangisidir (2024 itibarıyla)?", "o": ["Çin", "Hindistan", "ABD", "Endonezya"], "c": "Hindistan"},
        {"s": "Aşağıdakilerden hangisi bir işletim sistemi değildir?", "o": ["Linux", "Windows", "Python", "macOS"], "c": "Python"},
        {"s": "Hangi kuş türü uçamaz?", "o": ["Saka", "Deve Kuşu", "Martı", "Pelikan"], "c": "Deve Kuşu"},
        {"s": "Hangi ülkenin resmi dili Portekizce'dir?", "o": ["Arjantin", "Brezilya", "Meksika", "Şili"], "c": "Brezilya"}
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# --- OYUN DURUMU ---
if 'secili_sorular' not in st.session_state:
    havuz = get_tum_sorular()
    st.session_state.secili_sorular = random.sample(havuz, min(len(havuz), 12))
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.joker_erdal = True
    st.session_state.gizli_siklar = []

# --- ARAYÜZ ---
st.markdown('<h2 style="text-align:center; color:#11114e;">💰 Milyoner</h2>', unsafe_allow_html=True)

if not st.session_state.elendi and st.session_state.index < 12:
    soru = st.session_state.secili_sorular[st.session_state.index]
    mevcut_odul = oduller[st.session_state.index]
    
    st.markdown(f'<div class="reward-banner">🏆 Soru: {st.session_state.index + 1}/12 | Ödül: {mevcut_odul}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        with (col1 if i % 2 == 0 else col2):
            if opt in st.session_state.gizli_siklar:
                st.button(" ", disabled=True, key=f"empty_{i}_{st.session_state.index}")
            else:
                if st.button(opt, key=f"btn_{i}_{st.session_state.index}"):
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
    st.write("---")
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
                st.info(f"Erdal Kanki: Doğru cevap kesinlikle '{soru['c']}'!")
                time.sleep(2)
                st.session_state.index += 1
                st.session_state.joker_erdal = False
                st.session_state.gizli_siklar = []
                st.rerun()

elif st.session_state.elendi:
    st.error(f"Elendiniz! Ödül: {oduller[st.session_state.index-1] if st.session_state.index > 0 else '0 TL'}")
    if st.button("🔄 Yeniden Başla"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.balloons()
    st.success("1 MİLYON TL KAZANDINIZ!")
    if st.button("🎮 Tekrar Oyna"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
