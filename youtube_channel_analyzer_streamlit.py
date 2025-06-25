import streamlit as st
import pandas as pd
import requests
import json
import time
import os
from datetime import datetime
import re

# Configuration
st.set_page_config(
    page_title="YouTube Channel Analyzer",
    page_icon="🎬",
    layout="wide"
)

class YouTubeAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def extract_channel_info(self, url):
        """Extract channel ID or video ID from various YouTube URL formats"""
        patterns = [
            (r'youtube\.com/channel/([a-zA-Z0-9_-]+)', 'channel'),
            (r'youtube\.com/c/([a-zA-Z0-9_-]+)', 'username'),
            (r'youtube\.com/user/([a-zA-Z0-9_-]+)', 'username'),
            (r'youtube\.com/@([a-zA-Z0-9_-]+)', 'handle'),
            (r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', 'video'),
            (r'youtu\.be/([a-zA-Z0-9_-]+)', 'video'),
            (r'youtube\.com/embed/([a-zA-Z0-9_-]+)', 'video')
        ]

        for pattern, type_name in patterns:
            match = re.search(pattern, url)
            if match:
                return {'id': match.group(1), 'type': type_name}
        return None

    def get_channel_by_id(self, channel_id):
        """Get channel data by channel ID"""
        try:
            url = f"{self.base_url}/channels"
            params = {
                'part': 'snippet,statistics',
                'id': channel_id,
                'key': self.api_key
            }
            response = requests.get(url, params=params)

            # Check for API errors
            if response.status_code == 403:
                error_data = response.json()
                if 'quotaExceeded' in str(error_data):
                    st.error("🚨 **YouTube API kvóta byla vyčerpána!** Zkuste to zítra nebo použijte jiný API klíč.")
                    return None
                else:
                    st.error(f"🚨 **API chyba 403:** {error_data.get('error', {}).get('message', 'Neznámá chyba')}")
                    return None
            elif response.status_code == 400:
                error_data = response.json()
                st.error(f"🚨 **Neplatná URL nebo parametry:** {error_data.get('error', {}).get('message', 'Zkontrolujte formát URL')}")
                return None
            elif response.status_code != 200:
                st.error(f"🚨 **YouTube API chyba {response.status_code}:** Zkuste to později")
                return None

            data = response.json()
            return data.get('items', [None])[0]
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 **Chyba připojení:** {str(e)}")
            return None
        except Exception as e:
            st.error(f"🚨 **Neočekávaná chyba:** {str(e)}")
            return None

    def get_video_info(self, video_id):
        """Get video data and extract channel ID"""
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet',
                'id': video_id,
                'key': self.api_key
            }
            response = requests.get(url, params=params)

            # Check for API errors
            if response.status_code == 403:
                error_data = response.json()
                if 'quotaExceeded' in str(error_data):
                    st.error("🚨 **YouTube API kvóta byla vyčerpána!** Zkuste to zítra nebo použijte jiný API klíč.")
                    return None
                else:
                    st.error(f"🚨 **API chyba 403:** {error_data.get('error', {}).get('message', 'Neznámá chyba')}")
                    return None
            elif response.status_code != 200:
                st.error(f"🚨 **YouTube API chyba {response.status_code}:** Zkuste to později")
                return None

            data = response.json()
            video = data.get('items', [None])[0]
            if video:
                return video['snippet']['channelId']
            return None
        except Exception as e:
            st.error(f"🚨 **Chyba při získávání video dat:** {str(e)}")
            return None

    def get_channel_videos(self, channel_id, max_results=5):
        """Get recent videos from channel"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'channelId': channel_id,
                'type': 'video',
                'order': 'date',
                'maxResults': max_results,
                'key': self.api_key
            }
            response = requests.get(url, params=params)

            if response.status_code == 403:
                error_data = response.json()
                if 'quotaExceeded' in str(error_data):
                    st.error("🚨 **YouTube API kvóta byla vyčerpána!** Zkuste to zítra nebo použijte jiný API klíč.")
                    return []
            elif response.status_code != 200:
                return []

            data = response.json()
            return data.get('items', [])
        except Exception:
            return []

def load_api_key():
    """Load API key from various sources"""
    # Try Streamlit secrets first
    if 'youtube_api_key' in st.secrets:
        return st.secrets['youtube_api_key']

    # Try local file
    if os.path.exists('api_key.txt'):
        try:
            with open('api_key.txt', 'r') as f:
                key = f.read().strip()
                if key and key != 'YOUR_YOUTUBE_DATA_API_KEY_HERE':
                    return key
        except:
            pass

    return None

def load_classification_words():
    """Load classification words from file or defaults"""
    default_words = {
        'kids': ['kids', 'children', 'toys', 'cartoon', 'animation', 'disney', 'nursery', 'děti', 'dětský', 'hračky', 'pohádky', 'animace', 'animovaný', 'kreslený', 'detský', 'rozprávky', 'detské'],
        'teen': ['teen', 'gaming', 'minecraft', 'fortnite', 'tiktok', 'challenge', 'prank', 'vlog', 'youtuberi', 'youtuber', 'gaming', 'hry', 'challenge', 'výzva', 'teenage', 'teenageři', 'mladí', 'mládež'],
        'serious': ['news', 'business', 'science', 'technology', 'education', 'documentary', 'research', 'university', 'zprávy', 'věda', 'technologie', 'vzdělávání', 'univerzita', 'výzkum', 'business', 'správy', 'veda', 'technológie', 'vzdelávanie', 'univerzita', 'výskum']
    }

    if os.path.exists('classification_words.json'):
        try:
            with open('classification_words.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass

    return default_words

def save_classification_words(words):
    """Save classification words to file"""
    try:
        with open('classification_words.json', 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def classify_channel(channel_data, videos, classification_words):
    """Classify channel based on content"""
    if not channel_data:
        return {'kids': 0, 'teen': 0, 'serious': 0, 'primary_category': 'Unknown'}

    # Combine text from channel and videos
    text_parts = [
        channel_data['snippet']['title'],
        channel_data['snippet']['description']
    ]

    for video in videos:
        text_parts.append(video['snippet']['title'])
        text_parts.append(video['snippet']['description'])

    text = ' '.join(text_parts).lower()

    # Count keyword matches
    scores = {'kids': 0, 'teen': 0, 'serious': 0}

    for word in classification_words['kids']:
        scores['kids'] += len(re.findall(re.escape(word.lower()), text))

    for word in classification_words['teen']:
        scores['teen'] += len(re.findall(re.escape(word.lower()), text))

    for word in classification_words['serious']:
        scores['serious'] += len(re.findall(re.escape(word.lower()), text))

    # Normalize scores
    total = sum(scores.values()) or 1
    normalized_scores = {k: round((v / total) * 100) for k, v in scores.items()}

    # Determine primary category
    max_score = max(normalized_scores.values())
    if max_score > 40:
        primary_category = max(normalized_scores, key=normalized_scores.get).title()
    else:
        primary_category = 'Mixed'

    return {**normalized_scores, 'primary_category': primary_category}

# Main app
def main():
    st.title("🎬 YouTube Channel Analyzer")
    st.markdown("Analyzujte YouTube kanály a videa pro optimalizaci Google Ads kampaní")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Konfigurace")

        # API Key section
        st.subheader("🔑 API Klíč")
        saved_api_key = load_api_key()

        if saved_api_key:
            st.success("✅ API klíč načten automaticky")
            api_key = saved_api_key
            if st.button("📝 Změnit API klíč"):
                st.session_state.show_api_input = True
        else:
            st.session_state.show_api_input = True

        if st.session_state.get('show_api_input', False) or not saved_api_key:
            api_key = st.text_input("YouTube Data API klíč:", type="password", 
                                   help="Získejte klíč z Google Cloud Console")
            if api_key and st.button("💾 Uložit klíč"):
                with open('api_key.txt', 'w') as f:
                    f.write(api_key)
                st.success("✅ API klíč uložen!")
                st.session_state.show_api_input = False
                st.rerun()

        # Classification words section
        st.subheader("🏷️ Klasifikační slova")
        classification_words = load_classification_words()

        kids_words = st.text_area("Dětské kanály:", 
                                 value=', '.join(classification_words['kids']),
                                 height=100)
        teen_words = st.text_area("Teen kanály:", 
                                 value=', '.join(classification_words['teen']),
                                 height=100)
        serious_words = st.text_area("Seriózní obsah:", 
                                    value=', '.join(classification_words['serious']),
                                    height=100)

        if st.button("💾 Uložit klasifikační slova"):
            new_words = {
                'kids': [w.strip() for w in kids_words.split(',') if w.strip()],
                'teen': [w.strip() for w in teen_words.split(',') if w.strip()],
                'serious': [w.strip() for w in serious_words.split(',') if w.strip()]
            }
            if save_classification_words(new_words):
                st.success("✅ Slova uložena!")
            else:
                st.error("❌ Chyba při ukládání")

    # Main content
    if not locals().get('api_key'):
        st.error("⚠️ Zadejte YouTube Data API klíč v postranním panelu")
        return

    # Input tabs
    tab1, tab2 = st.tabs(["📝 Ruční zadání URL", "📊 CSV soubor"])

    with tab1:
        st.subheader("YouTube URL (kanály nebo videa)")
        st.markdown("Zadejte URL oddělené novými řádky. Podporované formáty:")
        st.code("""https://www.youtube.com/@channel
https://www.youtube.com/channel/UC...
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID""")

        # Změna: TextArea místo text_input pro více URL
        url_input = st.text_area("URL seznam:", 
                                placeholder="Zadejte URL oddělené novými řádky",
                                height=150)

        if st.button("🚀 Analyzovat URL", type="primary"):
            if url_input:
                urls = [url.strip() for url in url_input.split('\n') if url.strip()]
                if urls:
                    analyze_urls(urls, api_key, classification_words)
                else:
                    st.warning("⚠️ Zadejte alespoň jednu platnou URL")
            else:
                st.warning("⚠️ Zadejte alespoň jednu URL")

    with tab2:
        st.subheader("CSV soubor z Google Ads")
        uploaded_file = st.file_uploader("Vyberte CSV soubor", type=['csv'])

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("📋 Náhled dat:")
                st.dataframe(df.head())

                url_column = st.selectbox("Vyberte sloupec s YouTube URL:", df.columns)

                if st.button("🚀 Analyzovat CSV", type="primary"):
                    urls = df[url_column].dropna().astype(str).tolist()
                    urls = [url.strip() for url in urls if url.strip() and url != 'nan']
                    if urls:
                        analyze_urls(urls, api_key, classification_words)
                    else:
                        st.warning("⚠️ Ve vybraném sloupci nejsou žádné platné URL")
            except Exception as e:
                st.error(f"❌ Chyba při načítání CSV: {str(e)}")

def analyze_urls(urls, api_key, classification_words):
    """Analyze list of URLs"""
    analyzer = YouTubeAnalyzer(api_key)
    results = []

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, url in enumerate(urls):
        progress = (i + 1) / len(urls)
        progress_bar.progress(progress)
        status_text.text(f"Analyzuji {i + 1}/{len(urls)}: {url[:50]}...")

        try:
            # Extract channel info
            extracted = analyzer.extract_channel_info(url)
            if not extracted:
                st.warning(f"⚠️ Neplatná URL: {url}")
                continue

            channel_id = extracted['id']

            # If it's a video, get channel ID
            if extracted['type'] == 'video':
                channel_id = analyzer.get_video_info(extracted['id'])
                if not channel_id:
                    continue
            elif extracted['type'] in ['username', 'handle']:
                # For usernames and handles, we need to search
                st.warning(f"⚠️ Nepodporovaný formát URL (použijte Channel ID): {url}")
                continue

            # Get channel data
            channel_data = analyzer.get_channel_by_id(channel_id)
            if not channel_data:
                continue

            # Get recent videos
            videos = analyzer.get_channel_videos(channel_id)

            # Classify
            classification = classify_channel(channel_data, videos, classification_words)

            # Store result
            result = {
                'URL': url,
                'Channel Title': channel_data['snippet']['title'],
                'Subscribers': int(channel_data['statistics'].get('subscriberCount', 0)),
                'Videos': int(channel_data['statistics'].get('videoCount', 0)),
                'Views': int(channel_data['statistics'].get('viewCount', 0)),
                'Primary Category': classification['primary_category'],
                'Kids %': classification['kids'],
                'Teen %': classification['teen'],
                'Serious %': classification['serious']
            }
            results.append(result)

        except Exception as e:
            st.error(f"❌ Chyba při analýze {url}: {str(e)}")

        # Small delay to respect API limits
        time.sleep(0.1)

    # Clear progress
    progress_bar.empty()
    status_text.empty()

    # Display results
    if results:
        display_results(results)
    else:
        st.warning("⚠️ Žádné výsledky k zobrazení")

def display_results(results):
    """Display analysis results"""
    st.success(f"✅ Analýza dokončena! Zpracováno {len(results)} kanálů")

    # Summary statistics
    df = pd.DataFrame(results)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kids_count = len(df[df['Primary Category'] == 'Kids'])
        st.metric("🧸 Dětské kanály", kids_count)
    with col2:
        teen_count = len(df[df['Primary Category'] == 'Teen'])
        st.metric("🎮 Teen kanály", teen_count)
    with col3:
        serious_count = len(df[df['Primary Category'] == 'Serious'])
        st.metric("📰 Seriózní kanály", serious_count)
    with col4:
        mixed_count = len(df[df['Primary Category'] == 'Mixed'])
        st.metric("🔀 Smíšené kanály", mixed_count)

    # Detailed results
    st.subheader("📊 Detailní výsledky")

    # Add color coding
    def color_category(val):
        colors = {
            'Kids': 'background-color: #d4edda',
            'Teen': 'background-color: #fff3cd', 
            'Serious': 'background-color: #f8d7da',
            'Mixed': 'background-color: #e2e3e5'
        }
        return colors.get(val, '')

    styled_df = df.style.map(color_category, subset=['Primary Category'])
    st.dataframe(styled_df, use_container_width=True)

    # Export functionality
    csv = df.to_csv(index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Stáhnout výsledky (CSV)",
        data=csv,
        file_name=f"youtube_analysis_{timestamp}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    # Initialize session state
    if 'show_api_input' not in st.session_state:
        st.session_state.show_api_input = False

    main()
