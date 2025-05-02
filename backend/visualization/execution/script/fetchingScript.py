import json

def get_text_script(json_path):
    """
    Reads a JSON file and returns the 'script' value.
    
    Args:
        json_path (str): Full path to the JSON file.
    
    Returns:
        str: The script text extracted from the JSON.
    """
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data.get("script", "")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading script: {e}")
        return ""
