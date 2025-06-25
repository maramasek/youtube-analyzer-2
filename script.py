# Nejdříve si přečtu existující HTML soubor, abych pochopil jeho strukturu
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Zobrazím první část HTML souboru pro pochopení struktury
print("První část HTML souboru:")
print(html_content[:1000])
print("...")
print("Celková délka HTML souboru:", len(html_content))