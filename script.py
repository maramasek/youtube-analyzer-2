# Vytvoření souboru s předvyplněnými klasifikačními slovy
import json

# Definice klasifikačních slov pro různé kategorie
classification_words = {
    "kids": {
        "en": ["kids", "children", "toy", "cartoon", "animation", "disney", "baby", "nursery", "rhyme", "playground", "fairy", "lego", "preschool", "kindergarten", "child", "toddler"],
        "cs": ["děti", "dětský", "dětská", "hračky", "animovaný", "pohádka", "pohádky", "školka", "škola", "učení", "písničky", "říkanky", "pro děti", "dětské", "malé děti", "mateřská", "rýmy"],
        "sk": ["deti", "detský", "detská", "hračky", "animovaný", "rozprávka", "rozprávky", "škôlka", "škola", "učenie", "pesničky", "riekanky", "pre deti", "detské", "malé deti", "materská"]
    },
    "teen": {
        "en": ["teen", "teenager", "gaming", "tiktok", "challenge", "kpop", "makeup", "vlog", "prank", "minecraft", "fortnite", "roblox", "meme", "reaction", "unboxing"],
        "cs": ["teen", "teenager", "hry", "herní", "výzva", "výzvy", "móda", "líčení", "make-up", "trendy", "reakce", "vtipné", "challenge", "tiktok", "youtuberi", "youtubeři", "vlog", "střední škola", "střední", "spolužáci"],
        "sk": ["teen", "teenager", "hry", "herný", "výzva", "výzvy", "móda", "líčenie", "make-up", "trendy", "reakcie", "vtipné", "challenge", "tiktok", "youtuberi", "vlog", "stredná škola", "stredná", "spolužiaci"]
    },
    "serious": {
        "en": ["news", "business", "science", "technology", "research", "professional", "education", "documentary", "interview", "analysis", "politics", "economics", "history", "lecture", "tutorial"],
        "cs": ["zprávy", "podnikání", "věda", "technologie", "výzkum", "profesionální", "vzdělávání", "dokument", "rozhovor", "analýza", "politika", "ekonomika", "historie", "přednáška", "návod", "tutoriál", "univerzita", "vysoká škola"],
        "sk": ["správy", "podnikanie", "veda", "technológia", "výskum", "profesionálny", "vzdelávanie", "dokument", "rozhovor", "analýza", "politika", "ekonomika", "história", "prednáška", "návod", "tutoriál", "univerzita", "vysoká škola"]
    }
}

# Uložení klasifikačních slov do JSON souboru
with open('classification_words.json', 'w', encoding='utf-8') as json_file:
    json.dump(classification_words, json_file, ensure_ascii=False, indent=4)

print("Soubor classification_words.json byl úspěšně vytvořen.")

# Vytvoření souboru pro ukládání API klíče
with open('api_key.txt', 'w') as f:
    f.write("ZADEJTE_VAS_API_KLIC_ZDE")

print("Soubor api_key.txt byl úspěšně vytvořen.")

# Ukázat strukturu souborů
classification_words_content = json.dumps(classification_words, ensure_ascii=False, indent=4)
print("\nObsah souboru classification_words.json:")
print(classification_words_content)