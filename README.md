# Academic Website Generator for WordPress

A lightweight, YAML-based static website generator designed predominantly for academic websites. This tool converts simple YAML data files into a professional academic website without requiring direct HTML manipulation. The current version was descigned specifically for [LPAC](https://sites.psu.edu/eecslpac/) at Penn State though it can be easily adapted.

## Quick Start

1. Edit YAML files in `content/`:
   - `datasets.yaml` - Dataset directory
   - `news.yaml` - News and events 
   - `people.yaml` - Lab members and alumni
   - `publications.yaml` - Publications list
   - `research.yaml` - Research projects
   - `projects/*.yaml` - Individual project pages
   - `datasets/*.yaml` - Individual dataset pages

2. Generate HTML:
```bash
python generate_people.py --yaml_path data/people.yml --output_path output/people.html
python generate_publications.py --yaml_path data/publications.yml --output_path output/publications.html 
python generate_research.py --yaml_path data/research.yml --output_path output/research.html
python generate_datasets.py --yaml_path data/datasets.yml --output_path output/datasets.html
python generate_news.py --yaml_path data/news.yml --output_path output/news.html

python generate_project.py --yaml_path data/projects/vision_to_dyanmics.yml --output_path output/projects/vision_to_dynamics.html
python generate_individual_dataset.py --yaml_path data/datasets/psuhub.yml --output_path output/datasets/PSUHub.html
```

## Local Development

```
.
├── content/           # YAML content files
├── assets/         # CSS and images
│   └── images/
|     └── ...
│   └── custom.css
├── scripts/        # Python generators
└── output/         # Generated HTML
```

Serve the site locally in any way you prefer. For example, using Python's built-in HTTP server:
```bash
python -m http.server
# Visit http://localhost:8000/output/
```

## WordPress Integration

1. Copy `assets/custom.css` content into WordPress Customizer → Additional CSS
2. For each generated HTML file:
   - Copy content between `<body>` tags. You should exclude the <navbar> sections as this is just to aid in local development.
   - Paste into WordPress page using Code Editor.

Both the custom css file and enabling the code editor in WordPress may require additional plugins.

## Customization

Modify the YAML files to customize content while maintaining the required fields for each type. See example YAML files in `content/` for reference.