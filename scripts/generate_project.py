import yaml
from pathlib import Path
import argparse

project_template = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="/assets/custom.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <div class="project-page-container">
        <h1 class="project-page-title">{title}</h1>
        {content}
        {funding_section}
    </div>
</body>
</html>'''

def generate_members_section(data):
    """Generates HTML for members and collaborators along with institution key."""
    # Collect unique institutions and assign them numbers
    institution_map = {}
    institution_counter = 1
    for member in data.get('members', []):
        inst = member.get('institution', '')
        if inst and inst not in institution_map:
            institution_map[inst] = institution_counter
            institution_counter += 1

    # Separate collaborators from core members
    core_members = [m for m in data.get('members', []) if m.get('role') != 'Collaborator']
    collaborators = [m for m in data.get('members', []) if m.get('role') == 'Collaborator']

    # Generate HTML for core members
    core_members_html = "".join([f'''
        <div class="member-card">
            <a href="{member.get('link', '#')}">
                <img src="{member['image']}" alt="{member['name']}">
            </a>
            <a href="{member.get('link', '#')}">
                {member['name']}<sup>{institution_map.get(member.get("institution", ""), "")}</sup>
            </a>
            
        </div>
    ''' for member in core_members])

    # Generate HTML for collaborators in a separate row
    collaborators_html = "".join([f'''
        <div class="member-card">
            <a href="{member.get('link', '#')}">
                <img src="{member['image']}" alt="{member['name']}">
            </a>
            <a href="{member.get('link', '#')}">
                {member['name']}<sup>{institution_map.get(member.get("institution", ""), "")}</sup>
            </a>
            <div class="member-role">Collaborator</div>
        </div>
    ''' for member in collaborators])

    # Institution key in a single line
    institution_key_html = ", ".join([
        f'<sup>{num}</sup> [{inst}]'
        for inst, num in institution_map.items()
    ])

    return f'''
        <div class="project-page-section">
            <div class="project-members">{core_members_html}</div>
            <div class="collaborator-row">{collaborators_html}</div>
            <div class="institution-key">{institution_key_html}</div>
        </div>
    '''


def generate_datasets_section(data):
    """Generates HTML for datasets section."""
    if not data.get('datasets'):
        return ""

    datasets_html = "".join([f'''
        <div class="dataset-card">
            <h2 class="dataset-name">{dataset['name']} Dataset</h2>
            {f'<div class="dataset-image"><img src="{dataset["image"]}" alt="{dataset["name"]} visualization"></div>' if dataset.get('image') else ''}
            <div class="dataset-text">
                <div class="dataset-description">{dataset['description']}</div>
                {f'<div class="dataset-actions"><a href="{dataset["url"]}" class="dataset-link">[Access Dataset]</a></div>' if dataset.get('url') else ''}
                {f'<div class="citation-block"><pre class="dataset-citation">{dataset["citation"]}</pre></div>' if dataset.get('citation') else ''}
            </div>
        </div>
    ''' for dataset in data['datasets']])

    return f'<div class="project-page-section"><h1 class="page-section-title">Datasets</h1>{datasets_html}</div>'

def generate_presentations_section(data):
    """Generates HTML for presentations section."""

    if not data.get('presentations'):
        return ''
    
    presentations_html = ""

    for presentation in data['presentations']:
        # Boilerplate code for the each presentation block
        presentation_html = f'''
            <div class="abstract-card">
                <div class="abstract-content">
                    <div class="abstract-info">
                        <h2 class="abstract-title">{presentation['title']}</h2>
                        <div class="abstract-metadata">
                            <p>{presentation['authors']}</p>
                            <p>{presentation['publisher']}</p>
                            <p>{presentation['location']}</p>
                        </div>'''

        # If contains an abstract, add that in
        if presentation.get('abstract'):
            presentation_html += f'''<h3 style="font-size: medium; font-weight: bold; margin-top: 20px;">Abstract:</h3>
                    <div class="abstract-desc"> 
                        <span>{presentation['abstract']}</span>
                        <a href="{presentation['abstract_link']}" rel="noopener">
                            [Read Full]
                        </a> 
                    </div>'''
        else:
            presentation_html += '<h3 style="font-size: medium; font-weight: bold; margin-top: 20px;">[No Abstract]</h3>'
        
        presentation_html += '</div>'

        # If contains a poster, add that in
        if presentation.get('poster'):
            presentation_html += f'''<a href="{presentation['link']}" rel="noopener" class="abstract-doc">
                <img src="{presentation['poster']}" alt="Poster">
                </a>'''

        presentation_html += '</div></div>'
        presentations_html += presentation_html

    return f'<div class="project-page-section"><h1 class="page-section-title">Presentations</h1><div class="abstract-list">{presentations_html}</div></div>'

def generate_abstracts_section(data):
    """Generates HTML for abstracts section."""

    if not data.get('abstracts'):
        return ''
    
    abstracts_html = ""

    for abstract in data['abstracts']:
        # Boilerplate code for the each abstract block
        abstract_html = f'''
            <div class="abstract-card">
                <div class="abstract-content">
                    <div class="abstract-info">
                        <h2 class="abstract-title">{abstract['title']}</h2>
                        <div class="abstract-metadata">
                            <p>{abstract['authors']}</p>
                            <p>{abstract['publisher']}</p>
                            <p>{abstract['location']}</p>
                        </div>'''

        # If contains an abstract, add that in
        if abstract.get('abstract'):
            abstract_html += f'''<h3 style="font-size: medium; font-weight: bold; margin-top: 20px;">Abstract:</h3>
                    <div class="abstract-desc"> 
                        <span>{abstract['abstract']}</span>
                        <a href="{abstract['abstract_link']}" rel="noopener">
                            [Read Full]
                        </a> 
                    </div>'''
        else:
            abstract_html += '<h3 style="font-size: medium; font-weight: bold; margin-top: 20px;">[No Abstract]</h3>'
        
        abstract_html += '</div>'

        # If contains a poster, add that in
        if abstract.get('poster'):
            abstract_html += f'''<a href="{abstract['link']}" rel="noopener" class="abstract-doc">
                <img src="{abstract['poster']}" alt="Poster">
                </a>'''

        abstract_html += '</div></div>'
        abstracts_html += abstract_html

    return f'<div class="project-page-section"><h1 class="page-section-title">Abstracts</h1><div class="abstract-list">{abstracts_html}</div></div>'


def generate_media_section(data):
    """Generates HTML for media section (images and videos)."""
    if not data.get('media'):
        return ""

    media_items = data['media']
    media_html = ""

    # Images
    if 'images' in media_items:
        image_html = "".join([f'''
            <div class="media-item">
                <img src="{img['path']}" alt="{img.get('caption', 'Media Image')}">
                {f'<div class="caption">{img["caption"]}</div>' if 'caption' in img else ''}
            </div>
        ''' for img in media_items['images']])
        media_html += f'<div class="media-grid">{image_html}</div>'

    # Videos
    if 'videos' in media_items:
        video_html = "".join([f'''
            <div class="media-item">
                <video controls>
                    <source src="{vid['url']}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                {f'<div class="caption">{vid["caption"]}</div>' if 'caption' in vid else ''}
            </div>
        ''' for vid in media_items['videos']])
        media_html += f'<div class="media-grid">{video_html}</div>'

    if data['media'].get('citations'):
        citation_html = "".join([f'''
            <div class="citation-item">{citation['desc']}</div>
        '''for citation in data['media']['citations']])
        
        media_html += f'<div class="citation-list">{"".join(citation_html)}</div>'

    return f'<div class="project-page-section"><h1 class="page-section-title">Media</h1>{media_html}</div>'


def generate_project_sections(data):
    """Generates HTML for the entire project page, including all sections."""
    sections = []

    # Add members section
    if data.get('members'):
        sections.append(generate_members_section(data))

    # Add description
    if data.get('description'):
        sections.append(f'<div class="project-page-section"><div class="project-page-description">{data["description"]}</div></div>')

    # Add datasets
    if data.get('datasets'):
        sections.append(generate_datasets_section(data))

    # Add media
    if data.get('media'):
        sections.append(generate_media_section(data))

    # Add publications
    if data.get('publications'):
        pubs_html = "".join([f'''
            <div class="publication-card">
                <a href="{pub['link']}">
                    <img src="{pub['thumbnail']}" alt="{pub['title']}">
                    <div class="publication-title">{pub['title']}</div>
                </a>
            </div>
        ''' for pub in data['publications']])
        sections.append(f'<div class="project-page-section"><h1 class="page-section-title">Publications</h1><div class="publications-list">{pubs_html}</div></div>')

    if data.get('presentations'):
        sections.append(generate_presentations_section(data))

    if data.get('abstracts'):
        sections.append(generate_abstracts_section(data))

    return "\n".join(sections)


def generate_funding_section(funding_data):
    if not funding_data:
        return ""
        
    funding_items = []
    for grant in funding_data:
        if grant.get('url') and grant.get('award'):
            funding_items.append(f'<a href="{grant["url"]}">NSF Award {grant["award"]}</a>')
        elif grant.get('award'):
            funding_items.append(f'NSF Award {grant["award"]}')
        elif grant.get('agency'):
            funding_items.append(grant['agency'])
    
    if funding_items:
        return '<div class="funding-note">This research is funded in part by ' + " and ".join(funding_items) + '</div>'
    return ""

def generate_project_page(yaml_file, output_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        content = generate_project_sections(data)
        funding_section = generate_funding_section(data.get('funding', []))
        
        html = project_template.format(
            title=data['title'],
            content=content,
            funding_section=funding_section
        )
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
    except Exception as e:
        print(f"Error generating project page: {str(e)}")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate project pages from YAML data")
    parser.add_argument("--yaml_path", type=str, help="Path to project YAML data file")
    parser.add_argument("--output_path", type=str, help="Output directory for generated HTML files")
    args = parser.parse_args()
    
    generate_project_page(args.yaml_path, args.output_path)