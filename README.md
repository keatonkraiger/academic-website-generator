# Academic Website Generator

A lightweight, YAML-based static website generator designed specifically for academic websites. This tool converts simple YAML data files into a professional academic website without requiring direct HTML manipulation.

## Overview

This system generates academic-style web pages by:
- Storing content in maintainable YAML files
- Using Python scripts to convert YAML data into HTML
- Applying clean, academic-focused CSS styling
- Supporting WordPress integration

## Data Structure

### People Data (`people.yml`)
Manages all people associated with the lab in a single organized file:

```yaml
faculty:
  - name: Full Name
    status: faculty
    img: filename.jpg
    website: https://example.com
    email: email@university.edu
    education:
      - Ph.D. in Field, University
    info: Current Position/Role

current_students:
  - name: Student Name
    status: phd_student  # or ms_student, undergraduate
    img: filename.jpg
    education:
      - Degree Program

alumni:
  - name: Alumni Name
    status: alumni
    img: filename.jpg
    education:
      - Degree, University
    graduation_year: YYYY
    info: Current Position
```

Required fields: name, status, img, education
Optional fields: email, website, info, graduation_year

### Publications (`publist.yml`)
```yaml
- title: Publication Title
  image: image_filename.png
  description: Brief description
  authors: Author 1, Author 2
  month: 1-12
  year: YYYY
  link:
    display: Link Text
    url: https://publication-url
  publisher: Publisher Name
  highlight: 0 or 1  # Featured publication flag
  project_page: https://project-page-url or null
```

### Research Projects (`research.yml`)
```yaml
projects:
  ongoing:
    - name: Project Name
      img_url: image_url
      description: Project description
      project_url: project_webpage
      status: ongoing
  
  previous:
    - name: Project Name
      img_url: image_url
      description: Project description
      project_url: project_webpage
      status: previous
```

## Usage

### 1. Update YAML Files
Add or modify content in the appropriate YAML files following the structures above.

### 2. Generate HTML
```bash
python generate_people.py
python generate_publications.py
python generate_research.py
```

### 3. WordPress Integration
1. Copy generated HTML content
2. Paste into WordPress using the HTML editor
3. Ensure custom CSS is added to your WordPress theme

## CSS Integration

The system uses `custom.css` which provides:
- Academic-focused typography
- Responsive layouts for people, publications, and projects
- Support for profile photos and project images
- Clean, professional styling

## File Structure
```
.
├── data/
│   ├── people.yml
│   ├── publist.yml
│   └── research.yml
├── assets/
│   ├── images/
│   │   └── people/
│   └── custom.css
├── scripts/
│   └── generate_pages.py ...
└── pages/
    └── generated HTML files
```

## Requirements

- Python 3.x
- PyYAML library
- Web server or WordPress installation
- Basic understanding of YAML syntax

## WordPress Setup

1. Navigate to Appearance → Customize → Additional CSS
2. Copy the contents of `custom.css`
3. Paste into the Additional CSS section
4. Save changes