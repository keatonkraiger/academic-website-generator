import yaml
from bs4 import BeautifulSoup
from pathlib import Path

# --- CONFIG ---
html_path = "publications.html"  # Your HTML file
yaml_path = "content/publications.yml"             # Your YAML file
output_path = "content/publications_updated.yml"   # Output file with updated YAML

# --- LOAD HTML & YAML ---
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

with open(yaml_path, 'r', encoding='utf-8') as f:
    pubs = yaml.safe_load(f)

# --- PARSE HTML FOR TITLE → IMAGE MAP ---
html_pubs = {}
for entry in soup.select(".pub-entry"):
    title_tag = entry.select_one(".pub-title")
    img_tag = entry.select_one("img")
    if title_tag and img_tag:
        title = title_tag.text.strip()
        image_url = img_tag['src']
        html_pubs[title] = image_url

# --- UPDATE YAML ---
updated = 0
for pub in pubs:
    title = pub.get('title', '').strip()
    if title in html_pubs:
        pub['image'] = html_pubs[title]
        updated += 1

with open(output_path, 'w', encoding='utf-8') as f:
    yaml_str = yaml.dump(pubs, sort_keys=False, allow_unicode=True)
    entries = yaml_str.split('\n- ')  # Separate each top-level item
    spaced_yaml_str = '\n\n- '.join(entries)  # Add newline before each new item
    f.write(spaced_yaml_str)


print(f"✅ Updated {updated} entries with images.")
