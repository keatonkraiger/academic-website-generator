# Academic Website Generator

A lightweight, YAML-based static website generator designed specifically for academic websites. This tool converts simple YAML data files into a professional academic website without requiring direct HTML manipulation. The current version was descigned specifically for [LPAC](https://sites.psu.edu/eecslpac/) at Penn State.

## Quick Start

1. Edit YAML files in `data/`:
   - `people.yml` - Lab members and alumni
   - `publications.yml` - Publications list
   - `research.yml` - Research projects
   - `projects/*.yml` - Individual project pages

2. Generate HTML:
```bash
python generate_people.py --yaml_path data/people.yml --output_path output/people.html
python generate_publications.py --yaml_path data/publications.yml --output_path output/publications.html 
python generate_research.py --yaml_path data/research.yml --output_path output/research.html
python generate_project.py --yaml_path data/projects/example.yml --output_path output/projects/example.html
```

## Local Development

```
.
├── data/           # YAML content files
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
   - Copy content between `<body>` tags
   - Paste into WordPress page using Code Editor.

Both the custom css file and enabling the code editor in WordPress may require additional plugins.

## Customization

Modify the YAML files to customize content while maintaining the required fields for each type. See example YAML files in `data/` for reference.