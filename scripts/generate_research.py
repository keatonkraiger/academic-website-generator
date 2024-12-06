import yaml
from pathlib import Path
import argparse

# HTML templates
research_template = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="/assets/custom.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Projects</title>
</head>
<body>
    <div class="projects-wrapper">
        <div class="projects-container">
            <h1 class="section-title">Ongoing Projects</h1>
            {ongoing_projects}
            
            <h1 class="section-title">Previous Projects</h1>
            {previous_projects}
        </div>
    </div>
</body>
</html>'''

def format_project_card(project):
    card_html = f'''
        {"<a href='" + project['project_url'] + "'" if project.get('project_url') else "<div"} 
        class="project-listing-card">
            <img src="{project['img_url']}" alt="{project['name']}" class="project-listing-image">
            <div class="project-listing-content">
                <h2 class="project-listing-title">{project['name']}</h2>
                <p class="project-listing-description">{project['description']}</p>
            </div>
        {"</a>" if project.get('project_url') else "</div>"}'''
    return card_html

def generate_research_page(yaml_file, output_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        ongoing = "".join(format_project_card(p) for p in data['projects']['ongoing'])
        previous = "".join(format_project_card(p) for p in data['projects']['previous'])
        
        html = research_template.format(
            ongoing_projects=ongoing,
            previous_projects=previous
        )
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
    except Exception as e:
        print(f"Error generating research page: {str(e)}")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate research projects page from YAML data")
    argparser.add_argument('--yaml_path', type=str, help="Path to the YAML file containing research data")
    argparser.add_argument('--output_path', type=str, help="Path to the output HTML file")
    args = argparser.parse_args()
    
    generate_research_page(args.yaml_path, args.output_path)