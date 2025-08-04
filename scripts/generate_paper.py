from bs4 import BeautifulSoup
import yaml
from pathlib import Path
import argparse

navbar_html = """
<nav class="navbar">
  <div class="nav-container">
    <a href='index.html' class='nav-brand'>LPAC</a>
    <div class='nav-links'>
      <a href='../index.html'>Home</a>
      <a href='../local_output/people.html'>People</a>
      <a href='../local_output/research.html'>Research</a>
      <a href='../local_output/publications.html'>Publications</a>
      <a href='../local_output/news.html'>News</a>
      <a href='../local_output/datasets.html'>Datasets</a>
    </div>
  </div>
</nav>
"""

style_html = """
  .navbar {
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1rem;
  }
  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .nav-brand {
    font-size: 1.5rem;
    color: #1772d0;
    text-decoration: none;
    font-weight: bold;
  }
  .nav-links {
    display: flex;
    gap: 2rem;
  }
  .nav-links a {
    color: #1772d0;
    text-decoration: none;
    font-size: 1rem;
  }
  .nav-links a:hover {
    color: #f09228;
  }
  @media (max-width: 768px) {
    .nav-container {
      flex-direction: column;
      gap: 1rem;
    }
    .nav-links {
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }
  }
"""

html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"UTF-8\">
    <title>{title}</title>
    <link rel=\"stylesheet\" type=\"text/css\" href=\"../../assets/custom.css\">
    <style>{style}</style>
  </head>
  <body>
    {navbar}
    <div class=\"projects-wrapper\">
      <div class=\"projects-container\">
        <h1 class=\"section-title\">{title}</h1>
        {papers}
        {downloads}
      </div>
    </div>
  </body>
</html>
"""

def generate_links(links):
    if not links:
        return ""
    icons = {
        'paper': '📄',
        'poster': '🖼️',
        'github': '🐙'
    }
    links_html = " ".join([
        f'<a href="{url}" target="_blank">{icons.get(kind, kind)}</a>'
        for kind, url in links.items()
    ])
    return f'<div class="paper-links">{links_html}</div>'

def generate_authors(members):
    if not members:
        return ""
    authors_html = []
    for member in members:
        name = member['name']
        link = member.get('link', '').strip()
        if link:
            authors_html.append(f'<a href="{link}" target="_blank">{name}</a>')
        else:
            authors_html.append(f'{name}')
    return f'<div class="paper-authors">{", ".join(authors_html)}</div>'

def generate_content_section(content):
    if not content:
        return ""
    html_parts = []
    for item in content:
        if item['type'] == 'figure':
            html_parts.append(f'''<div class="wide-figure">
                <img src="{item['path']}" alt="Figure">
                {f'<p class="figure-caption">{item.get("caption", "")}</p>' if item.get("caption") else ''}
            </div>''')
        elif item['type'] == 'abstract':
            html_parts.append(f'''<div class="abstract-block">
              <h3>Abstract</h3>
              <p>{item['text']}</p>
            </div>''')
        elif item['type'] == 'citation':
            html_parts.append(f'''<div class="citation-block">
              <p><b>Citation:</b></p>
              <pre class="dataset-citation">{item['text']}</pre>
            </div>''')
        elif item['type'] == 'links':
            links_html = " ".join([
                f'<a href="{l["url"]}" target="_blank">[{l["label"]}]</a>'
                for l in item.get('items', [])
            ])
            html_parts.append(f'<div class="paper-content-links">{links_html}</div>')
    return "\n".join(html_parts)

def generate_papers_section(papers):
    sections = []
    for paper in papers:
        section = f'''<div class="paper-block">
            <h2 class="paper-title">{paper['title']}</h2>
            {generate_authors(paper.get('members'))}
            {generate_links(paper.get('links'))}
            {generate_content_section(paper.get('content'))}
          </div>'''
        sections.append(section)
    return "\n".join(sections)

def generate_download_card(dl):
    return f'''
    <div class="download-card">
      <div class="download-info">
        <p class="download-title">{dl['title']}</p>
        <p class="download-description">{dl['description']}</p>
        <p class="download-meta">{dl['format']}</p>
      </div>
      <div class="download-options">
        <a href="{dl['url']}" target="_blank" rel="noopener">Download</a>
      </div>
    </div>
    '''

def generate_downloads_section(downloads):
    if not downloads:
        return ""
    cards_html = "".join([generate_download_card(dl) for dl in downloads])
    return f'<div class="downloads-section"><h2>Related Datasets</h2>{cards_html}</div>'

def generate_papers_page(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    title = data['title']
    papers_html = generate_papers_section(data['papers'])
    downloads_html = generate_downloads_section(data.get('downloads'))

    html = html_template.format(
        title=title,
        style=style_html,
        navbar=navbar_html,
        papers=papers_html,
        downloads=downloads_html
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate papers page from YAML")
    parser.add_argument('--yaml_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    args = parser.parse_args()

    generate_papers_page(args.yaml_path, args.output_path)
