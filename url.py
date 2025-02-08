import yaml
import os

def update_image_urls(yaml_content):
    """
    Update image URLs in the YAML content to the new WordPress format.
    """
    base_url = "https://sites.psu.edu/eecslpac/files/2024/12/"
    
    # Helper function to update a single person's image URL
    def update_person(person):
        name = person['name']
        # Convert name to filename format (replace spaces with underscores)
        filename = name.replace(' ', '_') + '.jpg'
        # Update the image URL
        person['img'] = base_url + filename
        return person
    
    # Process each section of the YAML
    for section in ['faculty', 'current_students', 'alumni', 'visitors']:
        if section in yaml_content:
            yaml_content[section] = [update_person(person) for person in yaml_content[section]]
    
    return yaml_content

def main(input_file, output_file):
    # Read the existing YAML
    with open(input_file, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
    
    # Update the URLs
    updated_content = update_image_urls(content)
    
    # Write the updated YAML
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(updated_content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Update image URLs in YAML file')
    parser.add_argument('input_file', help='Path to input YAML file')
    parser.add_argument('output_file', help='Path to output YAML file')
    
    args = parser.parse_args()
    
    main(args.input_file, args.output_file)