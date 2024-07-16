import json
from ansible_inventory_logger import logger

def quote_for_json(value):
    """
    Converts a given value into a JSON-compatible string representation.
    
    Args:
    value (any): The value to be converted for JSON.
    
    Returns:
    str: A JSON-compatible string representation of the input value.
    """
    # If the value is a string, use json.dumps to ensure proper escaping
    if isinstance(value, str):
        return json.dumps(value)
    # For dicts, lists, or tuples, convert them to a JSON string and remove the outer quotes or brackets
    elif isinstance(value, (dict, list, tuple)):
        return json.dumps(value)[1:-1]
    # For booleans, convert directly to their lowercase string representation
    elif isinstance(value, bool):
        return str(value).lower()
    # For None, return 'null'
    elif value is None:
        return 'null'
    # For numerics and other types, return the string representation
    else:
        return str(value)

def extract_quoted_string(criteria, start_index):
    """
    Extract a string enclosed in quotes from the criteria.

    Args:
        criteria (str): The criteria containing the quoted string.
        start_index (int): The starting index of the quoted string.

    Returns:
        tuple: (str, int)
            - str: The extracted string without the surrounding quotes.
            - int: The index after the closing quote.
    """

    logger.verbose(f"Extracting quoted string: {criteria}")
    start_quote = criteria[start_index]
    i = start_index + 1
    escaped = False
    extracted_string = []

    while i < len(criteria):
        char = criteria[i]
        if escaped:
            extracted_string.append(char)
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == start_quote:
            break
        else:
            extracted_string.append(char)
        i += 1

    if i < len(criteria):
        i += 1  # Include the closing quote

    logger.verbose(f"Extracted: {criteria}")
    return ''.join(extracted_string), i


def skip_whitespace(criteria, start_index):
    """
    Skip whitespace characters in the criteria.

    Args:
        criteria (str): The criteria string.
        start_index (int): The starting index in the criteria.

    Returns:
        int: The new index position after skipping whitespace.
    """
    while start_index < len(criteria) and criteria[start_index].isspace():
        start_index += 1
    logger.verbose(f"Skipped whitespace, new position: {start_index}")
    return start_index

def merge_data(dict1: dict, dict2: dict) -> dict:
    """
    Merges two dictionaries together, combining keys and preserving values from both.
    If a key exists in both dictionaries, the values are merged recursively.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: The merged dictionary.
    """
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(value, dict):
                dict1[key] = merge_data(dict1[key], value)
            elif isinstance(dict1[key], list) and isinstance(value, list):
                dict1[key].extend(x for x in value if x not in dict1[key])
            elif dict1[key] != value:
                dict1[key] = value
        else:
            dict1[key] = value
    return dict1
