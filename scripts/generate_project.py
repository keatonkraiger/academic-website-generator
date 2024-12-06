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
        <div class="funding-note">{funding}</div>
    </div>
</body>
</html>'''


def generate_project_sections(data):
    sections = []
    # Members section
    if data.get('members'):
        members_html = "".join([f'''
            <div class="member-card">
                <img src="{member['image']}" alt="{member['name']}">
                <a href="{member.get('link', '#')}">{member['name']}</a>
                {f'<div class="member-role">{member["role"]}</div>' if 'role' in member else ''}
            </div>
        ''' for member in data['members']])
        sections.append(f'<div class="project-page-section"><div class="project-members">{members_html}</div></div>')

    # Description section
    if data.get('description'):
        sections.append(f'<div class="project-page-section"><div class="project-page-description">{data["description"]}</div></div>')

    # Media section
    if data.get('media'):
        media_items = []
        if data['media'].get('images'):
            media_items.extend([f'''
                <div class="media-item">
                    <img src="{img['path']}" alt="{img.get('caption', '')}">
                    {f"<div class='caption'>{img['caption']}</div>" if 'caption' in img else ''}
                </div>
            ''' for img in data['media']['images']])
            
        if data['media'].get('videos'):
            media_items.extend([f'''
                <div class="media-item video">
                    <iframe src="{video['url'].replace('watch?v=', 'embed/')}" frameborder="0" allowfullscreen></iframe>
                </div>
            ''' if 'youtube.com' in video['url'] else f'''
                <div class="media-item video">
                    <video controls poster="{video.get('thumbnail', '')}">
                        <source src="{video['url']}" type="video/mp4">
                    </video>
                </div>
            ''' for video in data['media']['videos']])
            
        if media_items:
            sections.append(f'<div class="project-page-section"><div class="media-grid">{"".join(media_items)}</div></div>')

    # Publications section
    if data.get('publications'):
        pubs_html = "".join([f'''
            <div class="publication-card">
                <a href="{pub['link']}">
                    <img src="{pub['thumbnail']}" alt="{pub['title']}">
                    <div class="publication-title">{pub['title']}</div>
                </a>
            </div>
        ''' for pub in data['publications']])
        sections.append(f'<div class="project-page-section"><div class="publications-list">{pubs_html}</div></div>')
    
    return "\n".join(sections)

def generate_project_page(yaml_file, output_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        content = generate_project_sections(data)
        funding = "This research is funded in part by " + " and ".join(
            f'<a href="{grant["url"]}">NSF Award {grant["award"]}</a>'
            for grant in data.get('funding', [])
        )
        
        html = project_template.format(
            title=data['title'],
            content=content,
            funding=funding
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
    
    generate_project_page(args.yml_path, args.out_path)