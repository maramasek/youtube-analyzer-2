# Vytvořím requirements.txt pro Streamlit deploy
requirements_txt = '''streamlit>=1.28.0
pandas>=1.5.0
requests>=2.28.0
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements_txt)

print("✅ Requirements.txt vytvořen pro Streamlit deploy")

# Vytvořím .streamlit/secrets.toml template
secrets_template = '''# Streamlit secrets template
# Pro nasazení na Streamlit Cloud přidejte tento klíč do secrets v nastavení aplikace

youtube_api_key = "YOUR_YOUTUBE_DATA_API_KEY_HERE"
'''

import os
os.makedirs('.streamlit', exist_ok=True)
with open('.streamlit/secrets.toml', 'w') as f:
    f.write(secrets_template)

print("✅ Secrets template vytvořen: .streamlit/secrets.toml")