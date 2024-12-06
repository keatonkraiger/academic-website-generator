import yaml
import argparse

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

    html_output = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="../assets/custom.css">
    <title>Publications</title>
</head>
<body>
    <div class="publications-container">'''
    
    for year in sorted(pubs_by_year.keys(), reverse=True):
        html_output += f'''
        <div class="pub-year">
            <h2>{year}</h2>
            <div class="pub-list">'''
        
        sorted_pubs = sorted(
            pubs_by_year[year],
            key=lambda x: x.get('month', 0) or 0,
            reverse=True
        )
        
        for pub in sorted_pubs:
            html_output += format_publication(pub)
            
        html_output += '</div></div>'
    
    html_output += '</div></body></html>'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate publications page from YAML data")
    parser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing publication data")
    parser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = parser.parse_args()
    
    generate_publications_page(args.yaml_path, args.output_path)