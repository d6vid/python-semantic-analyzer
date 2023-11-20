import literals_mapping
import re

def remove_element_from_list(list, element):
    if list is None:
        return -1
    return [x for x in list if x != element]

def get_last_element_that_is_not_specific_ones(list, not_ones):
    for element in reversed(list):
        if not element in not_ones:
            return element
    return None

def add_whitespace_between_specific_chars(input_string, chars_to_add_whitespace):
    result = ''
    for char in input_string:
        if char in chars_to_add_whitespace:
            result += f' {char} '
        else:
            result += char
    return result

def get_type_of_value(value):
    types = list(literals_mapping.references.keys())
    for type in types:
        if re.search(literals_mapping.references[type].value, value):
            return type

def get_information_from_txt(file_path):
    try:
        with open(file_path, 'r',  encoding='utf-8') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")