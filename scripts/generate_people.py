import yaml
import math
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
    <link rel=\"stylesheet\" type=\"text/css\" href=\"../assets/custom.css\">
    <style>{style}</style>
  </head>
  <body>
    {navbar}
    {body}
  </body>
</html>
"""

def format_person(person):
    education = person.get('education', [''])[0] if person.get('education') else ''
    link_start = f'<a href="{person["website"]}" target="_blank" rel="noopener">' if person.get('website') else '<a>'
    img_src = f"{person['img']}"
    return f'''<div class="person">{link_start}
<img src="{img_src}" alt="{person['name']}" />
<span class="person-name">{person['name']}</span>
<span class="person-edu">{education}</span>
</a></div>\n'''

def distribute_rows(items, max_per_row=5):
    total = len(items)
    if total <= max_per_row:
        return [total]
    factors = [i for i in range(2, min(max_per_row + 1, total + 1)) if total % i == 0]
    if factors:
        return [factors[-1]] * (total // factors[-1])
    rows = math.ceil(total / max_per_row)
    while rows <= total:
        per_row = math.ceil(total / rows)
        if per_row <= max_per_row:
            result = [per_row] * (rows - 1)
            remainder = total - (per_row * (rows - 1))
            if remainder > 0:
                result.append(remainder)
            return result
        rows += 1

def format_section(people, section_name):
    if not people:
        return ""
    row_distribution = distribute_rows(people)
    html = f'''<h2 style="text-align: center;"><span style="color: #055099;">{section_name}</span></h2>
<div class="people-container">\n'''
    current_idx = 0
    for row_size in row_distribution:
        html += '<div class="people-row">\n'
        for _ in range(row_size):
            if current_idx < len(people):
                html += format_person(people[current_idx])
                current_idx += 1
        html += '</div>\n'
    html += '</div>\n'
    return html

def generate_people_page(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    body = ""
    if data.get('faculty'):
        body += format_section(data['faculty'], "Faculty")
    if data.get('current_students'):
        body += format_section(data['current_students'], "Graduate Students")
    if data.get('alumni'):
        body += '<h2 style="text-align: center;"><span style="color: #055099;">Alumni</span></h2>'
        phd = [p for p in data['alumni'] if any('Ph.D.' in ed for ed in p['education'])]
        ms = [p for p in data['alumni'] if any('M.S.' in ed for ed in p['education'])]
        bs = [p for p in data['alumni'] if any('B.S.' in ed for ed in p['education'])]
        if phd: body += format_section(phd, "Ph.D. Alumni")
        if ms: body += format_section(ms, "M.S. Alumni")
        if bs: body += format_section(bs, "B.S. Alumni")
    if data.get('visitors'):
        body += format_section(data['visitors'], "Visitors")

    html = html_template.format(title="Lab Members", navbar=navbar_html, style=style_html, body=body)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate people page from YAML data")
    parser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing people data")
    parser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = parser.parse_args()

    generate_people_page(args.yaml_path, args.output_path)