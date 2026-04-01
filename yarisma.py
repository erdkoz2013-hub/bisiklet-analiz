import streamlit as st
import time
import random


# ==========================================
# ⚙️ SADECE BURADAKİ RAKAMLARI DEĞİŞTİR:
UST_BOSLUK = -140
KUTU_YUKSEKLIGI = 20   # Kutuların dikine boyu (70, 80, 90 dene)
YAZI_BOYUTU = 16       # Cevapların yazı büyüklüğü (14 veya 18 dene)
ARALIK_BOSLUGU = 5    # Kutuların arasındaki mesafe (5 veya 15 dene)
JOKER_MESAFESI = -10    
SORU_KUTUSU_BOYU = 20
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
        background-color: #f8f9fa; padding: 10px; border-radius: 10px;
        border: 2px solid #ffd700; text-align: center; margin-bottom: 10px;
        color: #11114e; font-weight: bold; font-size: 18px;
    }

    .question-box {
        background: linear-gradient(145deg, #11114e, #1e1e8e);
        padding: 15px; border-radius: 15px; color: white;
        text-align: center; font-size: 20px; font-weight: bold;
        margin-bottom: 15px; min-height: 100px; display: flex;
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
        {"s": "Periyodik tabloda oda sıcaklığında sıvı halde bulunan iki elementten biri cıvadır, diğeri hangisidir?", "o": ["Brom", "Sezyum", "Galyum", "Fransiyum"], "c": "Brom"},
        {"s": "Modern olimpiyat tarihindeki ilk altın madalyayı hangi branşta kim kazanmıştır?", "o": ["Üç Adım Atlama - James Connolly", "100m Koşu - Thomas Burke", "Disk Atma - Robert Garrett", "Eskrim - Leonidas Pyrgos"], "c": "Üç Adım Atlama - James Connolly"},
        {"s": "Dante'nin 'İlahi Komedya' eserinde rehberlik eden Latin şair kimdir?", "o": ["Horatius", "Vergilius", "Ovidius", "Cicero"], "c": "Vergilius"},
        {"s": "Dünyanın en derin noktası olan Mariana Çukuru'na inen ilk insan kimdir?", "o": ["James Cameron", "Don Walsh", "Jacques Piccard", "Jacques Cousteau"], "c": "Don Walsh"},
        {"s": "Hangi ülke Birleşmiş Milletler üyesi olmasına rağmen bayrağında ülke haritası yer almaz?", "o": ["Kıbrıs", "Kosova", "Kamboçya", "Antarktika"], "c": "Kamboçya"},
        {"s": "Satrançta 'Ölümsüz Oyun' olarak bilinen maç hangi iki oyuncu arasında oynanmıştır?", "o": ["Anderssen - Kieseritzky", "Morphy - Duke Karl", "Kasparov - Deep Blue", "Fischer - Spassky"], "c": "Anderssen - Kieseritzky"},
        {"s": "İnsan vücudunda kendi kendini yenileyemeyen tek hücre türü hangisidir?", "o": ["Karaciğer Hücresi", "Sinir Hücresi", "Deri Hücresi", "Kas Hücresi"], "c": "Sinir Hücresi"},
        {"s": "Nobel ödülünü reddeden ilk ve tek kişi kimdir?", "o": ["Jean-Paul Sartre", "Boris Pasternak", "Le Duc Tho", "Richard Kuhn"], "c": "Jean-Paul Sartre"},
        {"s": "Dünya üzerindeki en eski parlamento hangi ülkeye aittir?", "o": ["İngiltere", "İzlanda", "Yunanistan", "İtalya"], "c": "İzlanda"},
        {"s": "Işık hızını ilk kez yaklaşık olarak doğru hesaplayan bilim insanı kimdir?", "o": ["Ole Rømer", "Newton", "Einstein", "Fizeau"], "c": "Ole Rømer"},
        {"s": "Hangi elementin ismi Yunanca 'Yabancı' anlamına gelir?", "o": ["Argon", "Ksenon", "Neon", "Kripton"], "c": "Ksenon"},
        {"s": "Frida Kahlo'nun eşi olan ünlü Meksikalı ressam kimdir?", "o": ["Diego Rivera", "Salvador Dali", "Pablo Picasso", "Joan Miro"], "c": "Diego Rivera"},
        {"s": "Everest Dağı'na oksijen tüpü kullanmadan tırmanan ilk kişi kimdir?", "o": ["Edmund Hillary", "Reinhold Messner", "Tenzing Norgay", "Nimsdai Purja"], "c": "Reinhold Messner"},
        {"s": "İstiklal Marşı'nın bestecisi Osman Zeki Üngör, hangi enstrümanın virtüözüdür?", "o": ["Piyano", "Keman", "Viyolonsel", "Ud"], "c": "Keman"},
        {"s": "Güneş sisteminde kendi ekseni etrafında diğerlerinden ters yönde dönen gezegen hangisidir?", "o": ["Uranüs", "Venüs", "Neptün", "Satürn"], "c": "Venüs"},
        {"s": "Fatih Sultan Mehmet'in portresini yapan İtalyan ressam kimdir?", "o": ["Gentile Bellini", "Leonardo da Vinci", "Michelangelo", "Raphael"], "c": "Gentile Bellini"},
        {"s": "Hangi ülkenin bayrağı dörtgen (dikdörtgen veya kare) değildir?", "o": ["Nepal", "Butan", "İsviçre", "Vatikan"], "c": "Nepal"},
        {"s": "Mozart'ın bitiremeden öldüğü, öğrencisi Süssmayr tarafından tamamlanan eseri hangisidir?", "o": ["Don Giovanni", "Sihirli Flüt", "Requiem", "Figaro'nun Düğünü"], "c": "Requiem"},
        {"s": "Dünyanın en yüksek debili şelalesi hangisidir?", "o": ["Niagara", "Victoria", "Boyoma", "Angel"], "c": "Boyoma"},
        {"s": "Bilgisayar terminolojisinde 'Bug' terimini ilk kez kullanan kişi kimdir?", "o": ["Ada Lovelace", "Alan Turing", "Grace Hopper", "Bill Gates"], "c": "Grace Hopper"},
        {"s": "Atatürk'ün 'Nutuk' adlı eseri hangi yılları kapsar?", "o": ["1919-1923", "1919-1927", "1923-1938", "1915-1927"], "c": "1919-1927"},
        {"s": "Kutup yıldızı (Polaris) hangi takımyıldızın en parlak üyesidir?", "o": ["Büyük Ayı", "Küçük Ayı", "Cassiopeia", "Orion"], "c": "Küçük Ayı"},
        {"s": "Hangi hayvanın kalbi kafasındadır?", "o": ["Karides", "Ahtapot", "Deniz Yıldızı", "Yengeç"], "c": "Karides"},
        {"s": "Mona Lisa tablosunun kaşları neden yoktur?", "o": ["Rönesans modası", "Ressam unuttu", "Restorasyonda silindi", "Kasten çizilmedi"], "c": "Restorasyonda silindi"},
        {"s": "Dünyanın en küçük bağımsız devleti Vatikan'ın yüzölçümü yaklaşık ne kadardır?", "o": ["0.44 km2", "1.2 km2", "5 km2", "10 km2"], "c": "0.44 km2"},
        {"s": "Hangi ünlü besteci sağır olduktan sonra 9. Senfoni'yi bestelemiştir?", "o": ["Bach", "Beethoven", "Chopin", "Vivaldi"], "c": "Beethoven"},
        {"s": "Akyuvarların (Beyaz kan hücreleri) görevi nedir?", "o": ["Oksijen taşımak", "Pıhtılaşma", "Vücut savunması", "Besin taşıma"], "c": "Vücut savunması"},
        {"s": "Yüz yıl savaşları hangi iki ülke arasında yapılmıştır?", "o": ["Fransa-Almanya", "İngiltere-Fransa", "İspanya-Portekiz", "Roma-Kartaca"], "c": "İngiltere-Fransa"},
        {"s": "Modern hemşireliğin kurucusu Florence Nightingale, hangi savaş sırasında ünlenmiştir?", "o": ["I. Dünya Savaşı", "Kırım Savaşı", "Trablusgarp Savaşı", "Çanakkale Savaşı"], "c": "Kırım Savaşı"},
        {"s": "Hangi ülkenin internet alan adı uzantısı '.ch'dir?", "o": ["Çin", "İsviçre", "Çekya", "Şili"], "c": "İsviçre"},
        {"s": "Kanuni Sultan Süleyman'ın 'Muhibbi' mahlasıyla yazdığı şiirlerin toplandığı esere ne denir?", "o": ["Divan-ı Muhibbi", "Süleymanname", "Şairler Sultanı", "Hasbahçe"], "c": "Divan-ı Muhibbi"},
        {"s": "Atmosferdeki en bol bulunan gaz hangisidir?", "o": ["Oksijen", "Azot", "Karbondioksit", "Helyum"], "c": "Azot"},
        {"s": "Kendi adıyla anılan bir kanunla 'Kütle Çekimini' açıklayan bilim insanı kimdir?", "o": ["Galileo", "Kepler", "Newton", "Copernicus"], "c": "Newton"},
        {"s": "Yazılı tarihin ilk barış antlaşması hangisidir?", "o": ["Mondros", "Kadeş", "Lozan", "Uşi"], "c": "Kadeş"},
        {"s": "Hangi organımızda 'Gözyaşı Kanalları' bulunur?", "o": ["Burun", "Göz", "Kulak", "Ağız"], "c": "Göz"},
        {"s": "İlk Türkçe sözlük olan 'Divânu Lugâti't-Türk' kim tarafından yazılmıştır?", "o": ["Kaşgarlı Mahmud", "Yusuf Has Hacib", "Edip Ahmet Yükneki", "Hoca Ahmet Yesevi"], "c": "Kaşgarlı Mahmud"},
        {"s": "Hangi gezegenin 82 tane uydusu vardır?", "o": ["Jüpiter", "Satürn", "Uranüs", "Mars"], "c": "Satürn"},
        {"s": "Hangi ülke hem Asya hem de Avrupa kıtasında toprağı bulunmaz?", "o": ["Türkiye", "Rusya", "Kazakistan", "Azerbaycan"], "c": "Kazakistan"},
        {"s": "Titanik'in battığı yıl (1912) hangi Osmanlı Padişahı tahttaydı?", "o": ["II. Abdülhamid", "V. Mehmed Reşad", "VI. Mehmed Vahdeddin", "II. Mahmud"], "c": "V. Mehmed Reşad"},
        {"s": "Hangi spor dalında 'Ace' terimi kullanılır?", "o": ["Futbol", "Basketbol", "Tenis", "Voleybol"], "c": "Tenis"},
        {"s": "Asal sayılar dizisindeki tek çift sayı hangisidir?", "o": ["0", "2", "4", "6"], "c": "2"},
        {"s": "Hangi ünlü ressamın tam adı 'Pablo Diego José Francisco de Paula Juan Nepomuceno María de los Remedios Cipriano de la Santísima Trinidad Ruiz y Picasso'dur?", "o": ["Dali", "Goya", "Picasso", "Velazquez"], "c": "Picasso"},
        {"s": "Türkiye'nin en yüksek dağı olan Ağrı Dağı'nın yüksekliği kaç metredir?", "o": ["5137", "5122", "5000", "4800"], "c": "5137"},
        {"s": "İnsan vücudundaki en uzun kemik hangisidir?", "o": ["Kaval Kemiği", "Uyluk Kemiği", "Omurga", "Pazı Kemiği"], "c": "Uyluk Kemiği"},
        {"s": "Nobel ödülleri hangi ülkede dağıtılmaktadır?", "o": ["Norveç-İsveç", "İsviçre-Fransa", "Almanya-Danimarka", "ABD-İngiltere"], "c": "Norveç-İsveç"},
        {"s": "Hangi ilimizde 'Dünyanın en büyük kanyonu' olarak bilinen kanyonlardan biri olan Valla Kanyonu bulunur?", "o": ["Uşak", "Kastamonu", "Antalya", "Muğla"], "c": "Kastamonu"},
        {"s": "Türkiye Cumhuriyeti'nin ilk Genelkurmay Başkanı kimdir?", "o": ["Kazım Karabekir", "İsmet İnönü", "Fevzi Çakmak", "Rauf Orbay"], "c": "Fevzi Çakmak"},
        {"s": "Hangi gezegenin bir günü, bir yılından daha uzundur?", "o": ["Merkür", "Venüs", "Mars", "Jüpiter"], "c": "Venüs"},
        {"s": "Osmanlı İmparatorluğu'nda 'Lale Devri' hangi antlaşma ile başlamıştır?", "o": ["Pasarofça", "Karlofça", "Zitvatorok", "İstanbul"], "c": "Pasarofça"},
        {"s": "Mona Lisa tablosu hangi müzede sergilenmektedir?", "o": ["Uffizi", "Louvre", "Prado", "British Museum"], "c": "Louvre"},
        {"s": "Tuncay ağanın lakabı nedir?", "o": ["Hızlı Gonzales", "Turbo", "Martı", "Yaralı Ceylan"], "c": "Turbo"},
        {"s": "G.D.G nin Büyük başkanı kimdir?", "o": ["Ajda Pekkan", "Reis", "Martı Janıtın", "Hüseyin Ovnamak"], "c": "Hüseyin Ovnamak"},
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
st.markdown('<h2 style="text-align:center; color:#11114e;">💰 Kim Milyoner</h2>', unsafe_allow_html=True)

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
