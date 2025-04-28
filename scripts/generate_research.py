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
        <h1 class=\"section-title\">Ongoing Projects</h1>
        {ongoing}
        <h1 class=\"section-title\">Previous Projects</h1>
        {previous}
      </div>
    </div>
  </body>
</html>
"""

def format_project_card(project):
    return f'''
    {"<a href='" + project['project_url'] + "'" if project.get('project_url') else "<div"} 
    class="project-listing-card">
        <img src="{project['img_url']}" alt="{project['name']}" class="project-listing-image">
        <div class="project-listing-content">
            <h2 class="project-listing-title">{project['name']}</h2>
            <p class="project-listing-description">{project['description']}</p>
        </div>
    {"</a>" if project.get('project_url') else "</div>"}
    '''

def generate_research_page(yaml_file, output_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    ongoing = "".join(format_project_card(p) for p in data['projects']['ongoing'])
    previous = "".join(format_project_card(p) for p in data['projects']['previous'])

    html = html_template.format(
        title="Research Projects",
        navbar=navbar_html,
        style=style_html,
        ongoing=ongoing,
        previous=previous
    )

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)    

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate research projects page from YAML data")
    argparser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing research data")
    argparser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = argparser.parse_args()

    generate_research_page(args.yaml_path, args.output_path)