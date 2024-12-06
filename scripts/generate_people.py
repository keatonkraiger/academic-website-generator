import yaml
import math

def format_person(person):
    """Format a single person's HTML with name, image, and education info."""
    # Get the first education entry if it exists
    education = person.get('education', [''])[0] if person.get('education') else ''
    
    # Construct link with website if available, otherwise no link
    link_start = f'<a href="{person["website"]}" target="_blank" rel="noopener">' if person.get('website') else '<a>'
    
    # Get image path - assuming images are in a standard location
    img_src = f"{person['img']}"
    
    return f'''<div class="person">{link_start}
<img src="{img_src}" alt="{person['name']}" />
<span class="person-name">{person['name']}</span>
<span class="person-edu">{education}</span>
</a></div>\n'''

def distribute_rows(items, max_per_row=5):
    """Calculate optimal distribution of items across rows."""
    total = len(items)
    if total <= max_per_row:
        return [total]
    
    # Try factors of total first
    factors = [i for i in range(2, min(max_per_row + 1, total + 1)) if total % i == 0]
    if factors:
        return [factors[-1]] * (total // factors[-1])
    
    # If no clean factors, find best distribution
    rows = math.ceil(total / max_per_row)
    while rows <= total:
        per_row = math.ceil(total / rows)
        if per_row <= max_per_row:
            result = [per_row] * (rows - 1)
            remainder = total - (per_row * (rows - 1))
            if remainder > 0:
                result.append(remainder)
            return result
        rows += 1

def format_section(people, section_name):
    """Format a section of people with proper row distribution."""
    if not people:
        return ""
        
    row_distribution = distribute_rows(people)
    html = f'''\n<!------------------------ {section_name} -------------------------------------------->
<h2 style="text-align: center;"><span style="color: #055099;">{section_name}</span></h2>
<div class="people-container">\n\n'''
    
    current_idx = 0
    for row_size in row_distribution:
        html += '<div class="people-row">\n'
        for _ in range(row_size):
            if current_idx < len(people):
                html += format_person(people[current_idx])
                current_idx += 1
        html += '</div>\n'
    
    html += '</div>\n\n'
    return html

def generate_people_page(people_file, output_file):
    """Generate the complete people page from the unified YAML file."""
    # Read YAML file
    with open(people_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    html_output = '''<!DOCTYPE html>
<html>
<head>
    <title>Lab Members</title>
    <link rel="stylesheet" type="text/css" href="../assets/custom.css">
</head>
<body>
'''
    
    # Faculty section
    if data.get('faculty'):
        html_output += format_section(data['faculty'], "Faculty")
    
    # Current students section
    if data.get('current_students'):
        html_output += format_section(data['current_students'], "Graduate Students")
    
    # Alumni section - group by degree type
    if data.get('alumni'):
        html_output += '<h2 style="text-align: center;"><span style="color: #055099;">Alumni</span></h2>'
        
        # Filter alumni by degree
        phd_alumni = [p for p in data['alumni'] if any('Ph.D.' in ed for ed in p['education'])]
        ms_alumni = [p for p in data['alumni'] if any('M.S.' in ed for ed in p['education'])]
        bs_alumni = [p for p in data['alumni'] if any('B.S.' in ed for ed in p['education'])]
        
        if phd_alumni:
            html_output += format_section(phd_alumni, "Ph.D. Alumni")
        if ms_alumni:
            html_output += format_section(ms_alumni, "M.S. Alumni")
        if bs_alumni:
            html_output += format_section(bs_alumni, "B.S. Alumni")
    
    # Visitors section
    if data.get('visitors'):
        html_output += format_section(data['visitors'], "Visitors")
    
    html_output += '</body>\n</html>'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
        
        
people_file = 'content/people.yml'
output_file = 'output/people.html'
generate_people_page(people_file, output_file)