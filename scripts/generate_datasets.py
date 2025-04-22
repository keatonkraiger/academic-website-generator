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
    <div class=\"projects-wrapper\">
      <div class=\"projects-container\">
        <h1 class=\"section-title\">Available Datasets</h1>
        {cards}
      </div>
    </div>
  </body>
</html>
"""

def format_dataset_card(ds):
    return f'''
    <div class="dataset-listing-card">
        <img src="{ds['img_url']}" alt="{ds['title']}" class="dataset-image-rect">
        <div class="dataset-listing-content">
            <h2 class="dataset-listing-title">{ds['title']}</h2>
            <p class="dataset-listing-description">{ds['description']}</p>
            <a href="{ds['dataset_url']}" class="dataset-listing-link">View Dataset</a>
        </div>
    </div>'''

def generate_dataset_directory(yaml_file, output_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    cards = "\n".join([format_dataset_card(ds) for ds in data['datasets']])

    html = html_template.format(
        title="Datasets",
        navbar=navbar_html,
        style=style_html,
        cards=cards
    )

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate dataset directory HTML")
    parser.add_argument("--yaml_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    args = parser.parse_args()

    generate_dataset_directory(args.yaml_path, args.output_path)
