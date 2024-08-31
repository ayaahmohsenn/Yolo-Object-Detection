import xml.etree.ElementTree as ET
import json
import os

def xml_to_custom_json(xml_file_path, base_url):
    """
    Convert a single XML annotation file to JSON format.
    
    Args:
    - xml_file_path: Path to the XML file.
    - base_url: Base URL for constructing image URLs.

    Returns:
    - A list of annotations in JSON format.
    """
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract filename and construct content URL
    filename = root.find('filename').text
    content_url = f"{base_url}/{filename}"

    # List to hold all annotations for the current XML file
    annotations = []

    # Extract image dimensions
    size = root.find('size')
    image_width = int(size.find('width').text)
    image_height = int(size.find('height').text)

    # Extract objects (annotations)
    for obj in root.findall('object'):
        label = [obj.find('name').text]  # Extract the label as a list
        points = []

        # Extract bounding box and convert to normalized coordinates
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # Normalize coordinates by image dimensions
        points.append({'x': xmin / image_width, 'y': ymin / image_height})
        points.append({'x': xmax / image_width, 'y': ymax / image_height})

        # Create annotation entry
        annotation_entry = {
            'label': label,
            'notes': '',
            'points': points,
            'imageWidth': image_width,
            'imageHeight': image_height
        }

        annotations.append(annotation_entry)

    # Construct the final JSON structure for this annotation
    json_entry = {
        'content': content_url,
        'annotation': annotations,
        'extras': None
    }

    return json_entry

def process_all_annotations_to_single_json(xml_folder, json_output_file, base_url):
    """
    Process all XML annotation files in a directory and convert them to a single JSON file.

    Args:
    - xml_folder: Directory containing XML annotation files.
    - json_output_file: Path to save the combined JSON output file.
    - base_url: Base URL for constructing image URLs.
    """
    # List to collect all annotations
    all_annotations = []

    # List all XML files in the given folder
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]

    # Loop through all XML files and process each one
    for xml_file in xml_files:
        xml_file_path = os.path.join(xml_folder, xml_file)

        # Convert XML to JSON format
        json_data = xml_to_custom_json(xml_file_path, base_url)

        # Add to the combined list
        all_annotations.append(json_data)

    # Write all annotations to the single JSON output file, one per line
    with open(json_output_file, 'w', encoding='utf-8') as json_file:
        for annotation in all_annotations:
            json.dump(annotation, json_file)
            json_file.write('\n')

    print(f"Successfully converted all XML files to JSON and saved to {json_output_file}")

# Example usage
xml_folder = 'C:/E/Personal/ML/archive/annotations'  # Replace with the path to your folder containing XML files
json_output_file = 'C:/E/Personal/ML/archive/images/Jason_annotation/combined_annotations.json'  # Output file path for combined JSON
base_url = '/content/drive/MyDrive/ML/Projects/5_Personality_Detection/images'  # Replace with your base URL

# Process all annotations and save to a single JSON file
process_all_annotations_to_single_json(xml_folder, json_output_file, base_url)
