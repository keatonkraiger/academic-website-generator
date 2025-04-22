import yaml
from pathlib import Path
import argparse

navbar_html = """
<nav class="navbar">
  <div class="nav-container">
    <a href='../../index.html' class='nav-brand'>LPAC</a>
    <div class='nav-links'>
      <a href='../../index.html'>Home</a>
      <a href='../../output/people.html'>People</a>
      <a href='../../output/research.html'>Research</a>
      <a href='../../output/publications.html'>Publications</a>
      <a href='../../output/news.html'>News</a>
      <a href='../../output/datasets.html'>Datasets</a>
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
  <link rel="stylesheet" type="text/css" href="../../assets/custom.css">
  <style>{style}</style>
</head>
<body>
  {navbar}
  <div class="project-page-container">
  
    <hr class="styled-hr" />
    <h1 class="project-page-title">
    {title}</h1>
    {funding_section}
    <hr class="styled-hr" />

    <div class="dataset-image">
      <img src="{image}" alt="{title} visualization" />
    </div>

    <div class="dataset-text">
      <div class="dataset-description">{description}</div>
      <div class="citation-block">
        <p>If you use this dataset for publication, we kindly ask you to attribute credit by citing the following:</p>
        <pre class="dataset-citation">{citation}</pre>
      </div>
    </div>

    <hr class="styled-hr" />
    <h2>Downloads</h2>
    <hr class="styled-hr" />
    <div class="download-link-list">
      {downloads}
    </div>
  </div>
</body>
</html>
"""

def generate_funding_section(funding):
    if not funding:
        return ""
    parts = []
    for grant in funding:
        if grant.get("url") and grant.get("award"):
            parts.append(f'{grant["agency"]} <a href="{grant["url"]}">{grant["award"]}</a>')
        elif grant.get("award"):
            parts.append(f'{grant["agency"]} {grant["award"]}')
        else:
            parts.append(f'{grant["agency"]}')
    return '<p class="acknowledgement-notes">This research is funded in part by ' + ", ".join(parts) + '.</p>'

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

def generate_dataset_page(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    html = html_template.format(
        style=style_html,
        navbar=navbar_html,
        title=data["title"],
        image=data["image"],
        description=data["description"],
        citation=data["citation"],
        funding_section=generate_funding_section(data.get("funding")),
        downloads="\n".join([generate_download_card(d) for d in data.get("downloads", [])])
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate individual dataset page")
    parser.add_argument('--yaml_path', type=str, required=True, help="Path to the dataset YAML file")
    parser.add_argument('--output_path', type=str, required=True, help="Path to save the HTML file")
    args = parser.parse_args()

    generate_dataset_page(args.yaml_path, args.output_path)
