
import streamlit as st
import pandas as pd
import json
import re
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Nastavení stránky
st.set_page_config(
    page_title="YouTube Channel Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funkce pro načtení API klíče
def load_api_key():
    # Zkusit načíst z secrets
    try:
        return st.secrets["youtube_api_key"]
    except:
        # Pokud není v secrets, zkusit načíst ze souboru
        try:
            with open('api_key.txt', 'r') as f:
                api_key = f.read().strip()
                if api_key and api_key != "ZADEJTE_VAS_API_KLIC_ZDE":
                    return api_key
        except:
            pass
    return None

# Funkce pro načtení klasifikačních slov
def load_classification_words():
    try:
        with open('classification_words.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Výchozí klasifikační slova, pokud soubor neexistuje
        return {
            "kids": {
                "en": ["kids", "children", "toy", "cartoon", "animation", "disney"],
                "cs": ["děti", "dětský", "dětská", "hračky", "pohádka"],
                "sk": ["deti", "detský", "detská", "hračky", "rozprávka"]
            },
            "teen": {
                "en": ["teen", "teenager", "gaming", "tiktok", "challenge"],
                "cs": ["teen", "teenager", "hry", "výzva", "tiktok"],
                "sk": ["teen", "teenager", "hry", "výzva", "tiktok"]
            },
            "serious": {
                "en": ["news", "business", "science", "technology", "research"],
                "cs": ["zprávy", "podnikání", "věda", "technologie"],
                "sk": ["správy", "podnikanie", "veda", "technológia"]
            }
        }

# Funkce pro uložení klasifikačních slov
def save_classification_words(words):
    with open('classification_words.json', 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

# Funkce pro uložení API klíče
def save_api_key(api_key):
    with open('api_key.txt', 'w') as f:
        f.write(api_key)

# Funkce pro extrakci ID kanálu z URL
def extract_channel_id(url):
    # Zkusit rozpoznat různé formáty URL
    channel_id_patterns = [
        r'youtube\.com\/channel\/([^\/\?]+)',  # https://www.youtube.com/channel/UC...
        r'youtube\.com\/c\/([^\/\?]+)',        # https://www.youtube.com/c/...
        r'youtube\.com\/user\/([^\/\?]+)',     # https://www.youtube.com/user/...
        r'youtube\.com\/@([^\/\?]+)'           # https://www.youtube.com/@...
    ]

    for pattern in channel_id_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Funkce pro extrakci ID videa z URL
def extract_video_id(url):
    # Zkusit rozpoznat různé formáty URL videa
    video_id_patterns = [
        r'youtube\.com\/watch\?v=([^&]+)',  # https://www.youtube.com/watch?v=...
        r'youtu\.be\/([^\/\?]+)',           # https://youtu.be/...
        r'youtube\.com\/embed\/([^\/\?]+)'  # https://www.youtube.com/embed/...
    ]

    for pattern in video_id_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Funkce pro získání kanálu z ID videa
def get_channel_from_video(youtube, video_id):
    try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if video_response['items']:
            channel_id = video_response['items'][0]['snippet']['channelId']
            return channel_id
        return None
    except HttpError as e:
        st.error(f"Chyba při získávání informací o videu: {e}")
        return None

# Funkce pro získání dat o kanálu
def get_channel_data(youtube, channel_id):
    try:
        channel_response = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()

        if not channel_response['items']:
            return None

        channel_info = channel_response['items'][0]
        channel_data = {
            'id': channel_id,
            'title': channel_info['snippet']['title'],
            'description': channel_info['snippet']['description'],
            'subscriberCount': channel_info['statistics'].get('subscriberCount', '0'),
            'videoCount': channel_info['statistics'].get('videoCount', '0'),
            'viewCount': channel_info['statistics'].get('viewCount', '0'),
            'url': f"https://www.youtube.com/channel/{channel_id}"
        }

        # Získat poslední videa z kanálu
        playlist_id = get_uploads_playlist_id(youtube, channel_id)
        if playlist_id:
            videos = get_recent_videos(youtube, playlist_id, max_results=10)
            channel_data['recent_videos'] = videos

        return channel_data
    except HttpError as e:
        st.error(f"Chyba při získávání informací o kanálu: {e}")
        return None

# Funkce pro získání ID playlistu s nahranými videi
def get_uploads_playlist_id(youtube, channel_id):
    try:
        response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        if response['items']:
            return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return None
    except HttpError as e:
        st.error(f"Chyba při získávání ID playlistu: {e}")
        return None

# Funkce pro získání posledních videí z playlistu
def get_recent_videos(youtube, playlist_id, max_results=10):
    try:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=max_results
        ).execute()

        videos = []
        for item in response.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet'].get('description', ''),
                'publishedAt': item['snippet']['publishedAt'],
                'videoId': item['snippet']['resourceId']['videoId']
            }
            videos.append(video_data)

        return videos
    except HttpError as e:
        st.error(f"Chyba při získávání videí: {e}")
        return []

# Funkce pro klasifikaci kanálu
def classify_channel(channel_data, classification_words):
    if not channel_data:
        return {}

    # Spojit všechny textové informace pro analýzu
    text_to_analyze = f"{channel_data['title']} {channel_data['description']}"

    # Přidat titulky videí
    if 'recent_videos' in channel_data:
        for video in channel_data['recent_videos']:
            text_to_analyze += f" {video['title']} {video['description']}"

    text_to_analyze = text_to_analyze.lower()

    # Počítat výskyty klíčových slov pro každou kategorii
    scores = {
        'kids': 0,
        'teen': 0,
        'serious': 0
    }

    # Počty klíčových slov pro normalizaci
    keyword_counts = {
        'kids': 0,
        'teen': 0,
        'serious': 0
    }

    # Projít všechny jazyky a klíčová slova
    for category in ['kids', 'teen', 'serious']:
        for lang in ['en', 'cs', 'sk']:
            keywords = classification_words[category][lang]
            keyword_counts[category] += len(keywords)

            for keyword in keywords:
                if keyword.lower() in text_to_analyze:
                    scores[category] += 1

    # Normalizovat skóre (převést na procenta)
    for category in scores:
        if keyword_counts[category] > 0:
            scores[category] = (scores[category] / keyword_counts[category]) * 100

    # Určit hlavní kategorii
    main_category = max(scores, key=scores.get)

    # Přidat skóre a hlavní kategorii do dat kanálu
    result = {
        'main_category': main_category,
        'kids_score': scores['kids'],
        'teen_score': scores['teen'],
        'serious_score': scores['serious']
    }

    return result

# Funkce pro zpracování URL nebo CSV souboru
def process_urls(youtube, urls, classification_words):
    results = []

    for url in urls:
        if not url:
            continue

        channel_id = extract_channel_id(url)

        # Pokud URL odkazuje na video, získat ID kanálu z videa
        if not channel_id:
            video_id = extract_video_id(url)
            if video_id:
                channel_id = get_channel_from_video(youtube, video_id)

        if channel_id:
            # Získat data o kanálu
            channel_data = get_channel_data(youtube, channel_id)

            if channel_data:
                # Klasifikovat kanál
                classification = classify_channel(channel_data, classification_words)

                # Připravit výsledek
                result = {
                    'Channel Name': channel_data['title'],
                    'URL': channel_data['url'],
                    'Subscribers': channel_data['subscriberCount'],
                    'Main Category': classification['main_category'].capitalize(),
                    'Kids Score (%)': round(classification['kids_score'], 2),
                    'Teen Score (%)': round(classification['teen_score'], 2),
                    'Serious Score (%)': round(classification['serious_score'], 2)
                }

                results.append(result)

    return pd.DataFrame(results)

# Hlavní funkce Streamlit aplikace
def main():
    st.title("🎬 YouTube Channel Analyzer")
    st.write("Analyzujte YouTube kanály a určete jejich cílovou skupinu.")

    # Načíst API klíč a klasifikační slova
    api_key = load_api_key()
    classification_words = load_classification_words()

    # Sidebar pro konfiguraci
    with st.sidebar:
        st.header("⚙️ Konfigurace")

        # Sekce pro API klíč
        st.subheader("API klíč")

        new_api_key = st.text_input(
            "YouTube Data API klíč", 
            value=api_key if api_key else "", 
            type="password",
            help="Získejte klíč na https://console.cloud.google.com/apis/credentials"
        )

        if new_api_key != api_key and new_api_key:
            save_api_key(new_api_key)
            api_key = new_api_key
            st.success("API klíč byl uložen!")

        # Sekce pro úpravu klasifikačních slov
        st.subheader("Klasifikační slova")

        # Vytvořit expander pro každou kategorii a jazyk
        for category in ["kids", "teen", "serious"]:
            with st.expander(f"Kategorie: {category.capitalize()}"):
                for lang in ["en", "cs", "sk"]:
                    st.write(f"Jazyk: {lang.upper()}")

                    # Spojit slova pro zobrazení v text_area
                    words_str = ", ".join(classification_words[category][lang])

                    # Text area pro úpravu slov
                    new_words = st.text_area(
                        f"Klíčová slova ({lang})", 
                        words_str,
                        key=f"{category}_{lang}"
                    )

                    # Aktualizovat klasifikační slova, pokud došlo ke změně
                    if new_words != words_str:
                        # Rozdělit slova podle čárky a odstranit mezery
                        classification_words[category][lang] = [word.strip() for word in new_words.split(",") if word.strip()]

        # Tlačítko pro uložení klasifikačních slov
        if st.button("Uložit klasifikační slova"):
            save_classification_words(classification_words)
            st.success("Klasifikační slova byla uložena!")

    # Hlavní část aplikace
    if not api_key:
        st.warning("⚠️ Prosím, zadejte YouTube Data API klíč v postranním panelu.")
        st.stop()

    # Inicializace YouTube API klienta
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Záložky pro různé možnosti vstupu
    tab1, tab2, tab3 = st.tabs(["🔗 URL Kanálu/Videa", "📁 CSV Soubor", "📊 Výsledky"])

    # Záložka pro URL
    with tab1:
        st.subheader("Zadejte URL YouTube kanálu nebo videa")

        url_input = st.text_input(
            "YouTube URL", 
            placeholder="https://www.youtube.com/channel/... nebo https://www.youtube.com/watch?v=..."
        )

        if st.button("Analyzovat URL", key="analyze_url"):
            if url_input:
                with st.spinner("Analyzuji kanál..."):
                    results_df = process_urls(youtube, [url_input], classification_words)

                    if not results_df.empty:
                        st.session_state['results_df'] = results_df
                        st.success(f"✅ Kanál úspěšně analyzován!")
                        st.dataframe(results_df)
                    else:
                        st.error("❌ Nepodařilo se analyzovat kanál. Zkontrolujte URL a API klíč.")
            else:
                st.warning("⚠️ Prosím, zadejte URL YouTube kanálu nebo videa.")

    # Záložka pro CSV soubor
    with tab2:
        st.subheader("Nahrajte CSV soubor s YouTube URL")

        uploaded_file = st.file_uploader("Vyberte CSV soubor", type=["csv"])

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)

                # Zobrazit náhled dat
                st.write("Náhled dat:")
                st.dataframe(df.head())

                # Nechat uživatele vybrat sloupec s URL
                url_column = st.selectbox(
                    "Vyberte sloupec obsahující YouTube URL",
                    df.columns.tolist()
                )

                if st.button("Analyzovat CSV", key="analyze_csv"):
                    urls = df[url_column].tolist()

                    if urls:
                        with st.spinner(f"Analyzuji {len(urls)} kanálů..."):
                            results_df = process_urls(youtube, urls, classification_words)

                            if not results_df.empty:
                                st.session_state['results_df'] = results_df
                                st.success(f"✅ {len(results_df)} kanálů úspěšně analyzováno!")
                                st.dataframe(results_df)
                            else:
                                st.error("❌ Nepodařilo se analyzovat kanály. Zkontrolujte URL a API klíč.")
                    else:
                        st.warning("⚠️ Nebyla nalezena žádná URL pro analýzu.")

            except Exception as e:
                st.error(f"❌ Chyba při načítání CSV souboru: {str(e)}")

    # Záložka pro výsledky
    with tab3:
        st.subheader("Výsledky analýzy")

        if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
            results_df = st.session_state['results_df']

            # Zobrazit výsledky
            st.dataframe(results_df)

            # Nabídnout export do CSV
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Stáhnout výsledky jako CSV",
                data=csv,
                file_name="youtube_channel_analysis.csv",
                mime="text/csv"
            )

            # Zobrazit graf rozložení kategorií
            st.subheader("Rozložení hlavních kategorií")
            category_counts = results_df['Main Category'].value_counts()
            st.bar_chart(category_counts)

        else:
            st.info("Žádné výsledky k zobrazení. Nejdříve analyzujte kanály na záložce URL nebo CSV.")

if __name__ == "__main__":
    main()
