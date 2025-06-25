# Vytvořím ještě krátký test script pro ověření funkčnosti
test_script = '''#!/usr/bin/env python3
"""
Test script pro YouTube Channel Analyzer
Ověří základní funkcionalitu bez skutečných API volání
"""

import os
import json

def test_file_structure():
    """Test existence všech potřebných souborů"""
    required_files = [
        'youtube_channel_analyzer_streamlit.py',
        'index.html', 
        'api_key.txt',
        'requirements.txt',
        'test_data.csv',
        'DEPLOY_README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Chybějící soubory: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Všechny požadované soubory existují")
        return True

def test_api_key_template():
    """Test API key template"""
    try:
        with open('api_key.txt', 'r') as f:
            content = f.read().strip()
        
        if content == 'YOUR_YOUTUBE_DATA_API_KEY_HERE':
            print("✅ API key template je správný")
            return True
        else:
            print(f"⚠️ API key template má neočekávaný obsah: {content}")
            return False
    except Exception as e:
        print(f"❌ Chyba při čtení API key: {e}")
        return False

def test_streamlit_secrets():
    """Test Streamlit secrets template"""
    try:
        secrets_path = '.streamlit/secrets.toml'
        if os.path.exists(secrets_path):
            with open(secrets_path, 'r') as f:
                content = f.read()
            
            if 'youtube_api_key' in content:
                print("✅ Streamlit secrets template je správný")
                return True
            else:
                print("❌ Streamlit secrets neobsahuje youtube_api_key")
                return False
        else:
            print("❌ Streamlit secrets soubor neexistuje")
            return False
    except Exception as e:
        print(f"❌ Chyba při čtení secrets: {e}")
        return False

def test_csv_format():
    """Test CSV test dat"""
    try:
        import pandas as pd
        df = pd.read_csv('test_data.csv')
        
        if 'URL' in df.columns and len(df) > 0:
            print(f"✅ Test CSV data jsou v pořádku ({len(df)} řádků)")
            return True
        else:
            print("❌ Test CSV data mají nesprávný formát")
            return False
    except Exception as e:
        print(f"❌ Chyba při čtení CSV: {e}")
        return False

def main():
    """Spustí všechny testy"""
    print("🧪 Spouštím testy aplikace...")
    print("-" * 50)
    
    tests = [
        test_file_structure,
        test_api_key_template, 
        test_streamlit_secrets,
        test_csv_format
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("-" * 50)
    print(f"📊 Výsledky: {passed}/{total} testů prošlo")
    
    if passed == total:
        print("🎉 Všechny testy prošly! Aplikace je připravena k použití.")
        print("\\n📋 Další kroky:")
        print("1. Nastavte YouTube Data API klíč v api_key.txt")
        print("2. Pro Streamlit: nahrejte na GitHub a nasaďte na share.streamlit.io")
        print("3. Pro HTML: otevřete index.html v prohlížeči")
    else:
        print("⚠️ Některé testy selhaly. Zkontrolujte chyby výše.")

if __name__ == "__main__":
    main()
'''

with open('test_app.py', 'w', encoding='utf-8') as f:
    f.write(test_script)

print("✅ Test script vytvořen: test_app.py")

# Spustím test
print("\n🧪 Spouštím test aplikace:")
exec(open('test_app.py').read())