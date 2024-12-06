import yaml
from pathlib import Path
import argparse

html_template =  \
    '''<!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/assets/custom.css">
    </head>
    <body>
    <div class="project-container">
        <h1 class="project-title">Project Title</h1>
        <!-- Content sections -->
        <div class="funding-note">
            <!-- Funding information here -->
        </div>
    </div>
    </body>
    </html>'''


def generate_project_page(project_data, output_path):
    with open(project_data, 'r') as f:
        data = yaml.safe_load(f)
    
    template = html_template
    sections_html = []
    
    # Members section
    if data.get('members'):
        members_html = "".join([f"""
            <div class="member-card">
                <img src="{member['image']}" alt="{member['name']}">
                <a href="{member.get('link', '#')}">{member['name']}</a>
                {f'<div class="member-role">{member["role"]}</div>' if 'role' in member else ''}
            </div>
        """ for member in data['members']])
        
        sections_html.append(f"""
        <div class="project-section">
            <div class="project-members">{members_html}</div>
        </div>
        """)

    # Description section
    if data.get('description'):
        sections_html.append(f"""
        <div class="project-section">
            <div class="project-description">
                {data['description']}
            </div>
        </div>
        """)

    # Media section
    if data.get('media') and (data['media'].get('images') or data['media'].get('videos')):
        media_content = []
        
        if data['media'].get('images'):
            media_content.extend([f"""
                <div class="media-item">
                    <img src="{img['path']}" alt="{img.get('caption', '')}">
                    {f"<div class='caption'>{img['caption']}</div>" if 'caption' in img else ''}
                </div>
            """ for img in data['media']['images']])
        
        if data['media'].get('videos'):
            for video in data['media']['videos']:
                if 'youtube.com' in video['url']:
                    media_content.append(f"""
                    <div class="media-item video">
                        <iframe src="{video['url'].replace('watch?v=', 'embed/')}" 
                                frameborder="0" allowfullscreen></iframe>
                    </div>
                    """)
                else:
                    media_content.append(f"""
                    <div class="media-item video">
                        <video controls poster="{video.get('thumbnail', '')}">
                            <source src="{video['url']}" type="video/mp4">
                        </video>
                    </div>
                    """)
        
        if media_content:
            sections_html.append(f"""
            <div class="project-section">
                <div class="media-grid">{''.join(media_content)}</div>
            </div>
            """)

    # Publications section
    if data.get('publications'):
        pubs_html = "".join([f"""
        <div class="publication-card">
            <a href="{pub['link']}">
                <img src="{pub['thumbnail']}" alt="{pub['title']}">
                <div class="publication-title">{pub['title']}</div>
            </a>
        </div>
        """ for pub in data['publications']])
        
        sections_html.append(f"""
        <div class="project-section">
            <div class="publications-list">{pubs_html}</div>
        </div>
        """)

    # Funding HTML
    funding_html = "This research is funded in part by " + " and ".join(
        [f'<a href="{grant["url"]}">NSF Award {grant["award"]}</a>'
         for grant in data.get('funding', [])]
    )

    # Replace content in template
    html = template.replace("Project Title", data['title'])
    html = html.replace("<!-- Content sections -->", "\n".join(sections_html))
    html = html.replace("<!-- Funding information here -->", funding_html)

    # Write output file
    with open(output_path, 'w') as f:
        f.write(html)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate project pages from YAML data")
    parser.add_argument("--yml_path", type=str, help="Path to project YAML data file")
    parser.add_argument("--out_path", type=str, help="Output directory for generated HTML files")
    args = parser.parse_args()
    
    generate_project_page(args.yml_path, args.out_path)