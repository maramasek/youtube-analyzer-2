# YouTube Channel Analyzer - Webová verze

## 🚀 Rychlé spuštění

1. **Získání YouTube Data API klíče:**
   - Jděte na [Google Cloud Console](https://console.cloud.google.com/)
   - Vytvořte nový projekt nebo vyberte existující
   - Povolte "YouTube Data API v3"
   - Vytvořte API klíč (Credentials > Create Credentials > API Key)

2. **Konfigurace API klíče:**
   - Otevřete soubor `api_key.txt`
   - Nahraďte `YOUR_YOUTUBE_DATA_API_KEY_HERE` vaším skutečným API klíčem
   - Uložte soubor

3. **Spuštění aplikace:**
   - Otevřete soubor `index.html` v jakémkoli moderním prohlížeči
   - Aplikace automaticky načte API klíč ze souboru `api_key.txt`

## 📋 Funkce aplikace

### ✅ Automatické načítání API klíče
- API klíč se načte automaticky ze souboru `api_key.txt`
- Možnost zadání klíče přímo v aplikaci
- Maskování klíče pro bezpečnost

### ✅ Podporované formáty URL
- **Kanálové URL:**
  - `https://www.youtube.com/@channel`
  - `https://www.youtube.com/channel/UC...`
  - `https://www.youtube.com/c/channel`
  - `https://www.youtube.com/user/username`

- **Video URL (automaticky najde kanál):**
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `https://www.youtube.com/embed/VIDEO_ID`

### ✅ Klasifikační algoritmus
- **Dětské kanály:** obsah pro děti 0-12 let
- **Teen kanály:** obsah pro teenagers 13-18 let  
- **Seriózní obsah:** zpravodajství, věda, business
- **Smíšený obsah:** kombinace kategorií

### ✅ Pokročilé funkce
- Úprava klasifikačních slov přímo v aplikaci
- České a slovenské varianty klíčových slov
- Import CSV souborů z Google Ads
- Export výsledků do CSV
- Procentuální skórování pro každou kategorii

## 🎯 Způsoby použití

### 1. Ruční zadání URL
- Zadejte YouTube URL (kanály nebo videa) do textového pole
- Každou URL na nový řádek
- Klikněte na "Analyzovat URL"

### 2. CSV soubor z Google Ads
- Exportujte placement data z Google Ads do CSV
- Nahrajte soubor do aplikace
- Vyberte sloupec obsahující YouTube URL
- Spusťte analýzu

### 3. Úprava klasifikačních slov
- V postranním panelu upravte seznamy klíčových slov
- Slova oddělujte čárkami
- Klikněte "Uložit slova" pro aktivaci změn

## 📊 Interpretace výsledků

### Kategorie kanálů:
- **Kids (Zelená):** Vysoké skóre pro dětský obsah
- **Teen (Žlutá):** Vysoké skóre pro teenagerský obsah
- **Serious (Červená):** Vysoké skóre pro seriózní obsah
- **Mixed (Šedá):** Kombinovaný nebo neutrální obsah

### Metriky:
- **Procentuální skóre:** Jak moc kanál odpovídá každé kategorii
- **Statistiky kanálu:** Počet odběratelů, videí a zhlédnutí
- **Primární kategorie:** Hlavní klasifikace na základě skóre

## 🔧 Technické informace

### Požadavky:
- Moderní webový prohlížeč (Chrome, Firefox, Safari, Edge)
- Připojení k internetu (pro YouTube API)
- YouTube Data API klíč

### API limity:
- YouTube Data API má denní kvóty
- Jedna analýza kanálu ~ 5-10 jednotek kvóty
- Standardní kvóta: 10,000 jednotek/den
- Možnost analýzy ~1,000-2,000 kanálů denně

### Bezpečnost:
- API klíč se ukládá pouze lokálně
- Žádná data se neodesílají na externí servery
- Veškerá komunikace pouze s YouTube API

## 🚨 Řešení problémů

### API klíč se nenačte:
- Zkontrolujte, že soubor `api_key.txt` je ve stejné složce jako `index.html`
- Ověřte, že soubor obsahuje pouze API klíč bez mezer
- Zadejte klíč ručně v aplikaci

### Chyby při analýze:
- Ověřte platnost YouTube Data API klíče
- Zkontrolujte formát zadaných URL
- Ujistěte se, že kanály/videa existují a jsou veřejné

### Výsledky nejsou přesné:
- Upravte klasifikační slova v postranním panelu
- Přidejte specifická slova pro vaši doménu
- Algoritmus funguje nejlépe s jasně definovaným obsahem

## 📈 Tips pro optimalizaci Google Ads

### Brand Safety:
- Vyloučte kanály s nevhodným obsahem
- Vytvořte placement exclusion lists
- Monitorujte nová umístění pravidelně

### Targeting optimalizace:
- Segmentujte kampaně podle věkových skupin
- Použijte různé kreativy pro různé kategorie
- Sledujte performance podle typu kanálu

### ROI maximalizace:
- Analyzujte korelaci mezi kategorií a conversion rate
- Adjustujte bidding podle typu obsahu
- Pravidelně aktualizujte analýzu kanálů