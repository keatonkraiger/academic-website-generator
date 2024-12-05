# Academic Website Generator

A lightweight, YAML-based static website generator designed specifically for academic websites. This tool was created for the LPAC lab and allows researchers and academic groups to maintain a professional web presence through simple data files, without dealing directly with HTML markup.

## Overview

This system generates academic-style web pages by:
- Storing content in easily maintainable YAML files
- Using Python scripts to convert YAML data into HTML
- Applying clean, academic-focused CSS styling
- Supporting WordPress integration

## Structure

### Data Storage
Content is stored in YAML files, including:
- `People.yml`: Faculty, students, alumni, scholars/researchers, etc.
- `publist.yml`: Publication listings
- `projects.yml`: Project portfolios

### Key Components
- Python conversion scripts
- Custom CSS for academic styling
- HTML templates
- WordPress integration support

## Usage

### 1. Data Entry
Add or update information in the appropriate YAML files:

```yaml
- name: John Doe
  photo: john_doe.jpg
  email: mailto:jdoe@university.edu
  link: http://example.com
  number_educ: 1
  education1: Ph.D. in Computer Science
```

### 2. Generate HTML
Run the Python script to convert YAML to HTML:

```python
python generate_pages.py
```

### 3. WordPress Integration
To use with WordPress:
1. Copy the contents between `<body>` tags from the generated HTML
2. Paste into a WordPress page using the HTML editor
3. Add the custom CSS to your WordPress theme's custom CSS section

## CSS Integration

The system uses a minimal CSS framework designed for academic websites, featuring:
- Clean, professional typography
- Responsive grid layouts
- Academic-specific styling (publications, people listings, etc.)
- Support for both light and dark themes

## WordPress Setup

1. Navigate to Appearance → Customize → Additional CSS
2. Copy the contents of `custom.css`
3. Paste into the Additional CSS section
4. Save changes

## Features

- Clean, academic-focused design
- Easy content management through YAML files
- Responsive layouts
- Publication listings
- People/team pages
- Project portfolios
- News/updates sections
- WordPress compatibility

## Requirements

- Python 3.x
- PyYAML library
- Web server or WordPress installation
- Basic understanding of YAML syntax
