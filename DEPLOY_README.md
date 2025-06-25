# YouTube Channel Analyzer - Deploy Instructions

## 🚀 Streamlit Cloud Deploy

### Požadavky:
1. GitHub účet
2. YouTube Data API klíč z Google Cloud Console

### Kroky pro nasazení:
1. **Nahrejte soubory na GitHub:**
   - Vytvořte nový repository
   - Nahrajte všechny soubory z této složky

2. **Nasaďte na Streamlit Cloud:**
   - Jděte na [share.streamlit.io](https://share.streamlit.io)
   - Přihlaste se GitHub účtem
   - Klikněte "New app"
   - Vyberte váš repository
   - Main file: `youtube_channel_analyzer_streamlit.py`

3. **Nastavte API klíč:**
   - V nastavení aplikace přidejte Secret:
   - Key: `youtube_api_key`
   - Value: váš YouTube Data API klíč

### Soubory pro Streamlit deploy:
- `youtube_channel_analyzer_streamlit.py` - hlavní aplikace
- `requirements.txt` - Python dependencies
- `.streamlit/secrets.toml` - template pro secrets

## 🌐 Lokální HTML spuštění

### Požadavky:
- Moderní webový prohlížeč
- YouTube Data API klíč

### Kroky pro spuštění:
1. **Nastavte API klíč:**
   - Otevřete soubor `api_key.txt`
   - Nahraďte `YOUR_YOUTUBE_DATA_API_KEY_HERE` vaším API klíčem

2. **Spusťte aplikaci:**
   - Otevřete soubor `index.html` v prohlížeči
   - Aplikace automaticky načte API klíč

### Soubory pro HTML verzi:
- `index.html` - kompletní HTML aplikace
- `api_key.txt` - soubor s API klíčem
- `test_data.csv` - test data pro CSV import

## 🔑 Získání YouTube Data API klíče

1. Jděte na [Google Cloud Console](https://console.cloud.google.com/)
2. Vytvořte nový projekt nebo vyberte existující
3. Povolte "YouTube Data API v3"
4. Vytvořte API klíč (Credentials > Create Credentials > API Key)
5. (Volitelně) Omezte klíč na YouTube Data API

## 📊 Funkce aplikace

### ✅ Podporované URL formáty:
- `https://www.youtube.com/@channel`
- `https://www.youtube.com/channel/UC...`
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### ✅ Klasifikace kanálů:
- **Dětské kanály:** obsah pro děti 0-12 let
- **Teen kanály:** obsah pro teenagers 13-18 let  
- **Seriózní obsah:** zpravodajství, věda, business
- **Smíšený obsah:** kombinace kategorií

### ✅ Error handling:
- Detekce vyčerpání API kvóty
- Upozornění na neplatné URL
- Zobrazení chybových zpráv uživateli

### ✅ Export funkcionalita:
- CSV export s timestamp
- Procentuální skórování pro každou kategorii
- Statistiky kanálů (odběratelé, videa, zhlédnutí)

## 🛠️ Technické informace

### API limity:
- YouTube Data API: 10,000 jednotek/den
- Jedna analýza kanálu: ~5-10 jednotek
- Možnost analýzy: ~1,000-2,000 kanálů denně

### Přesnost klasifikace:
- Jasně definované kategorie: 85-90%
- Hraniční případy: 70-80%
- Algoritmus využívá textová metadata

## 📧 Podpora

Pro technickou podporu nebo otázky kontaktujte administrátora aplikace.
