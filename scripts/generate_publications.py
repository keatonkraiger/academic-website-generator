import yaml
from datetime import datetime

def format_publication(pub):
    template = f'''<img class="wp-image-190 size-thumbnail alignleft" src="{pub['image']}" alt="" width="150" height="150" />
<p style="text-align: left; line-height: 1.2;">
<span style="color: #000000; font-family: helvetica, arial, sans-serif;"><strong>{pub['title']}</strong></span>
<span style="color: #000000; font-family: helvetica, arial, sans-serif;">{pub['authors']}</span>
<span style="font-family: helvetica, arial, sans-serif; color: #000000;"><strong>{pub['link']['display']}</strong></span>'''

    if pub.get('publisher'):
        template += f'\n<span style="font-family: helvetica, arial, sans-serif; color: #000000;">{pub["publisher"]}</span>'

    links = []
    if pub['link'].get('url'):
        links.append(f'<span style="font-family: helvetica, arial, sans-serif;"><a href="{pub["link"]["url"]}">[PDF]</a></span>')
    if pub.get('project_page'):
        links.append(f'<span style="font-family: helvetica, arial, sans-serif;"><a href="{pub["project_page"]}">[Project]</span></a>')
    
    template += ' ' + ' '.join(links) + '</p>\n\n&nbsp;\n&nbsp;\n&nbsp;\n\n'
    return template

def generate_publications_page(yaml_file, output_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        publications = yaml.safe_load(f)
    
    html_output = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="../assets/custom.css">
</head>
<body>
'''
    
    # Group publications by year
    pubs_by_year = {}
    for pub in publications:
        year = pub['year']
        if year not in pubs_by_year:
            pubs_by_year[year] = []
        pubs_by_year[year].append(pub)
    
    # Sort by year (descending) and month (descending)
    for year in sorted(pubs_by_year.keys(), reverse=True):
        html_output += f'\n<h2 style="text-align: center;">{year}</h2>\n'
        html_output += '<hr />\n'
        
        # Sort publications within year by month
        sorted_pubs = sorted(
            pubs_by_year[year],
            key=lambda x: x.get('month', 0) or 0,  # Handle None values
            reverse=True
        )
        
        for pub in sorted_pubs:
            html_output += format_publication(pub)
    
    html_output += '</body>\n</html>'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)

# Usage
yaml_file = 'old_files/publist.yml'
output_file = 'new_files/new_publications.html'
generate_publications_page(yaml_file, output_file)