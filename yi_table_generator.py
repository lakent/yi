#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

SHORTCODE_USED = []
FULL_CODE_LIST = []
COMPONENT_MAP = []


def get_key_from_component(component):
    for item in COMPONENT_MAP:
        if item[0] == component:
            return item[1]
    return ''

def generate_shortcode(code, index, max_len):
    currentCode = code[0:index]
    
    if currentCode in SHORTCODE_USED and index <= max_len:
        return generate_shortcode(code, index + 1, max_len)
    elif index > max_len:
        return code 
    else:
        SHORTCODE_USED.append(currentCode)
        return currentCode

def generate_full_codes(REPERTOIRE_LIST):
    global FULL_CODE_LIST
    FULL_CODE_LIST = []
    for item in REPERTOIRE_LIST:
        s = ''.join([get_key_from_component(ch) for ch in item[1]])
        new_item = [item[0], s]
        FULL_CODE_LIST.append(new_item)
    return FULL_CODE_LIST

def read_tab_delimited_file(path):
    try:
        readContent = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                l = line.split('\t')
                if len(l) >= 2 and l[0].strip():
                    l[1] = l[1].strip()
                    readContent.append([l[0].strip(), l[1]])
        return readContent
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return []

def create_character_order_map(path):
    char_order = {}
    try:
        order_index = 0
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                l = line.split('\t')
                if l and l[0].strip():
                    character = l[0].strip()
                    char_order[character] = order_index
                    order_index += 1
        return char_order
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return {}

def write_full_code_table(path):
    try:
        with open(path, "w", encoding='utf-8') as table_file:
            for i in FULL_CODE_LIST:
                character = i[0]
                code = i[1]
                table_file.write(f"{character}\t{code}\n")
    except Exception as e:
        print(f"Error writing full code table: {e}")

def write_short_code_table(path, max_len):
    try:
        with open(path, "w", encoding='utf-8') as table_file:
            for i in FULL_CODE_LIST:
                character = i[0]
                code = i[1]
                short_code = generate_shortcode(code, 2, max_len)
                table_file.write(f"{character}\t{short_code}\n")
    except Exception as e:
        print(f"Error writing short code table: {e}")


if __name__ == '__main__':
    
    COMPONENT_MAPPING_PATH = 'yi_components_mapping.txt'
    CHAR_REPERTOIRE_PATH = 'yi_spelling.txt'
    CHARACTER_ORDER_PATH = 'char_freq.txt'
    
    FULLCODE_TABLE_PATH = 'yi_fullcode_table.txt'
    SHORTCODE_TABLE_PATH = 'yi_table.txt'
    
    MAX_SHORTCODE_LENGTH = 6
    
    COMPONENT_MAP = read_tab_delimited_file(COMPONENT_MAPPING_PATH)
    print(f"Read component key mapping from: {COMPONENT_MAPPING_PATH}")

    REPERTOIRE_LIST = read_tab_delimited_file(CHAR_REPERTOIRE_PATH)
    print(f"Read character repertoire coding table from: {CHAR_REPERTOIRE_PATH}")

    char_order_map = create_character_order_map(CHARACTER_ORDER_PATH)
    
    if not char_order_map:
        print(f"Warning: Character order map is empty. Sorting will be skipped.")
    else:
        default_order = len(char_order_map)
        
        REPERTOIRE_LIST.sort(key=lambda item: char_order_map.get(item[0], default_order))
        print(f"Repertoire list sorted by character order based on {CHARACTER_ORDER_PATH}.")

    generate_full_codes(REPERTOIRE_LIST)
    print("Translated component sequences to full codes.")

    write_full_code_table(FULLCODE_TABLE_PATH)
    print("Wrote full code table to " + FULLCODE_TABLE_PATH)

    write_short_code_table(SHORTCODE_TABLE_PATH, MAX_SHORTCODE_LENGTH)
    print("Wrote short code table to " + SHORTCODE_TABLE_PATH)