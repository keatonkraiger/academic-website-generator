import yaml
from pathlib import Path

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

# def format_project(project):
#     if project['project_url']:
#         return f'''
#         <a href="{project['project_url']}" class="project-card">
#             <img src="{project['img_url']}" alt="{project['name']}" class="project-image">
#             <div class="project-content">
#                 <h2 class="project-title">{project['name']}</h2>
#                 <p class="project-description">{project['description']}</p>
#             </div>
#         </a>
#         '''
#     else:
#         return f'''
#         <div class="project-card">
#             <img src="{project['img_url']}" alt="{project['name']}" class="project-image">
#             <div class="project-content">
#                 <h2 class="project-title">{project['name']}</h2>
#                 <p class="project-description">{project['description']}</p>
#             </div>
#         </div>
#         '''

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


# def generate_research_page(yaml_file, output_file):
#     # Read YAML file
#     with open(yaml_file, 'r', encoding='utf-8') as f:
#         data = yaml.safe_load(f)

#     html_output = f'''<!DOCTYPE html>
#     <html>
#     <head>
#         <link rel="stylesheet" type="text/css" href="../assets/custom.css">
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Research Projects</title>
#     </head>
#     <body>
#         <div class="container">
#             <h1 class="section-title">Ongoing Projects</h1>
#             {"".join(format_project(project) for project in data['projects']['ongoing'])}
            
#             <h1 class="section-title">Previous Projects</h1>
#             {"".join(format_project(project) for project in data['projects']['previous'])}
#         </div>
#     </body>
#     </html>
#     '''
    
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write(html_output)

if __name__ == "__main__":
    yaml_file = "content/research.yml"
    output_file = "output/research.html"
    generate_research_page(yaml_file, output_file)