import yaml
from pathlib import Path
import argparse

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
    <meta charset=\"UTF-8\">
    <title>{title}</title>
    <link rel=\"stylesheet\" type=\"text/css\" href=\"../assets/custom.css\">
    <style>{style}</style>
  </head>
  <body>
    {navbar}
    <div class=\"project-page-container\">
      <h1 class=\"project-page-title\">{title}</h1>
      {body}
      {funding}
    </div>
  </body>
</html>
"""

def generate_members_section(data):
    institution_map = {}
    counter = 1
    for m in data.get('members', []):
        inst = m.get('institution', '')
        if inst and inst not in institution_map:
            institution_map[inst] = counter
            counter += 1

    core = [m for m in data.get('members', []) if m.get('role') != 'Collaborator']
    collab = [m for m in data.get('members', []) if m.get('role') == 'Collaborator']

    core_html = ''.join([f'''
      <div class="member-card">
        <a href="{m.get('link', '#')}"><img src="{m['image']}" alt="{m['name']}"></a>
        <a href="{m.get('link', '#')}">{m['name']}<sup>{institution_map.get(m.get('institution', ''), '')}</sup></a>
      </div>''' for m in core])

    collab_html = ''.join([f'''
      <div class="member-card">
        <a href="{m.get('link', '#')}"><img src="{m['image']}" alt="{m['name']}"></a>
        <a href="{m.get('link', '#')}">{m['name']}<sup>{institution_map.get(m.get('institution', ''), '')}</sup></a>
        <div class="member-role">Collaborator</div>
      </div>''' for m in collab])

    inst_html = ', '.join([f'<sup>{n}</sup> [{i}]' for i, n in institution_map.items()])

    return f'''<div class="project-page-section">
      <div class="project-members">{core_html}</div>
      <div class="collaborator-row">{collab_html}</div>
      <div class="institution-key">{inst_html}</div>
    </div>'''

def generate_datasets_section(data):
    if not data.get('datasets'):
        return ""

    cards = ''.join([f'''
      <div class="dataset-card">
        <h2 class="dataset-name">{ds['name']} Dataset</h2>
        {f'<div class="dataset-image"><img src="{ds["image"]}" alt="{ds["name"]} visualization"></div>' if ds.get('image') else ''}
        <div class="dataset-text">
          <div class="dataset-description">{ds['description']}</div>
          {f'<div class="dataset-actions"><a href="{ds["url"]}" class="dataset-link">Access Dataset</a></div>' if ds.get('url') else ''}
          {f'<div class="citation-block"><pre class="dataset-citation">{ds["citation"]}</pre></div>' if ds.get('citation') else ''}
        </div>
      </div>''' for ds in data['datasets']])

    return f'<div class="project-page-section"><h2>Datasets</h2>{cards}</div>'

def generate_media_section(data):
    if not data.get('media'):
        return ""

    media_html = ""
    if 'images' in data['media']:
        media_html += '<div class="media-grid">' + ''.join([f'''
          <div class="media-item">
            <img src="{img['path']}" alt="{img.get('caption', 'Media Image')}">
            {f'<p>{img["caption"]}</p>' if 'caption' in img else ''}
          </div>''' for img in data['media']['images']]) + '</div>'

    if 'videos' in data['media']:
        media_html += '<div class="media-grid">' + ''.join([f'''
          <div class="media-item">
            <video controls><source src="{vid['url']}" type="video/mp4">Your browser does not support the video tag.</video>
            {f'<p>{vid["caption"]}</p>' if 'caption' in vid else ''}
          </div>''' for vid in data['media']['videos']]) + '</div>'

    return f'<div class="project-page-section"><h2>Media</h2>{media_html}</div>'

def generate_project_sections(data):
    sections = []
    if data.get('members'):
        sections.append(generate_members_section(data))
    if data.get('description'):
        sections.append(f'<div class="project-page-section"><div class="project-page-description">{data["description"]}</div></div>')
    if data.get('datasets'):
        sections.append(generate_datasets_section(data))
    if data.get('media'):
        sections.append(generate_media_section(data))
    if data.get('publications'):
        pubs_html = ''.join([f'''
          <div class="publication-card">
            <a href="{pub['link']}">
              <img src="{pub['thumbnail']}" alt="{pub['title']}">
              <div class="publication-title">{pub['title']}</div>
            </a>
          </div>''' for pub in data['publications']])
        sections.append(f'<div class="project-page-section"><h2>Publications</h2><div class="publications-list">{pubs_html}</div></div>')
    return "\n".join(sections)

def generate_funding_section(funding_data):
    if not funding_data:
        return ""
    items = []
    for grant in funding_data:
        if grant.get('url') and grant.get('award'):
            items.append(f'<a href="{grant["url"]}">NSF Award {grant["award"]}</a>')
        elif grant.get('award'):
            items.append(f'NSF Award {grant["award"]}')
        elif grant.get('agency'):
            items.append(grant['agency'])
    if items:
        return '<div class="funding-note">This research is funded in part by ' + " and ".join(items) + '</div>'
    return ""

def generate_project_page(yaml_file, output_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    body = generate_project_sections(data)
    funding = generate_funding_section(data.get('funding', []))
    html = html_template.format(title=data['title'], navbar=navbar_html, style=style_html, body=body, funding=funding)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate project pages from YAML data")
    parser.add_argument("--yaml_path", type=str, help="Path to project YAML data file")
    parser.add_argument("--output_path", type=str, help="Output path for generated HTML file")
    args = parser.parse_args()
    generate_project_page(args.yaml_path, args.output_path)
