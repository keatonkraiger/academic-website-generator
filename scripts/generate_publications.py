import yaml
import argparse
from pathlib import Path

navbar_html = """
<nav class="navbar">
  <div class="nav-container">
    <a href='index.html' class='nav-brand'>LPAC</a>
    <div class='nav-links'>
      <a href='../index.html'>Home</a>
      <a href='../output/people.html'>People</a>
      <a href='../output/research.html'>Research</a>
      <a href='../output/publications.html'>Publications</a>
      <a href='../output/news.html'>News</a>
      <a href='../output/datasets.html'>Datasets</a>
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
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../assets/custom.css">
    <style>{style}</style>
  </head>
  <body>
    {navbar}
    <div class="publications-container">
      {body}
    </div>
  </body>
</html>
"""

def format_publication(pub):
    links = []
    if pub['link'].get('url'):
        links.append(f'<a href="{pub["link"]["url"]}" class="pub-link">[PDF]</a>')
    if pub.get('project_page'):
        links.append(f'<a href="{pub["project_page"]}" class="pub-link">[Project]</a>')
    links_html = ''.join(links)

    return f'''
    <div class="pub-entry">
        <div class="pub-thumbnail">
            <img src="{pub['image']}" alt="{pub['title']}" />
        </div>
        <div class="pub-details">
            <div class="pub-title">{pub['title']}</div>
            <div class="pub-authors">{pub['authors']}</div>
            <div class="pub-venue">{pub['link']['display']}</div>
            {f'<div class="pub-publisher">{pub["publisher"]}</div>' if pub.get('publisher') else ''}
            <div class="pub-links">{links_html}</div>
        </div>
    </div>'''

def generate_publications_page(yaml_file, output_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        publications = yaml.safe_load(f)

    pubs_by_year = {}
    for pub in publications:
        year = pub['year']
        if year not in pubs_by_year:
            pubs_by_year[year] = []
        pubs_by_year[year].append(pub)

    content = ""
    for year in sorted(pubs_by_year.keys(), reverse=True):
        content += f'<div class="pub-year">\n<h2>{year}</h2>\n<div class="pub-list">'
        for pub in sorted(pubs_by_year[year], key=lambda x: x.get('month', 0) or 0, reverse=True):
            content += format_publication(pub)
        content += '</div></div>'

    html = html_template.format(title="Publications", navbar=navbar_html, style=style_html, body=content)

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate publications page from YAML data")
    parser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing publication data")
    parser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = parser.parse_args()

    generate_publications_page(args.yaml_path, args.output_path)
