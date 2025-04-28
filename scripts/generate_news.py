from bs4 import BeautifulSoup
import argparse
import yaml
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
    <meta charset=\"UTF-8\">
    <title>{title}</title>
    <link rel=\"stylesheet\" type=\"text/css\" href=\"../assets/custom.css\">
    <style>{style}</style>
  </head>
  <body>
    {navbar}
    <div class=\"fullnews-container\">
      <h1 class=\"fullnews-header\">News</h1>
      <div class=\"fullnews-table-container\">
        <table class=\"fullnews-table\" border=\"0\">
          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </div>
  </body>
</html>
"""

def generate_news_page(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    rows = ""
    for item in data.get('news', []):
        date = item.get('date', '')
        title = item.get('title', '')
        content = item.get('content', '')
        rows += f'''
          <tr>
            <td class=\"news-date\">{date}</td>
            <td class=\"news-content\">
              <strong>{title}</strong><br>{content}
            </td>
          </tr>
        '''

    html = html_template.format(
        title="News",
        navbar=navbar_html,
        style=style_html,
        rows=rows
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate news page from YAML data")
    parser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing news data")
    parser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = parser.parse_args()

    generate_news_page(args.yaml_path, args.output_path)