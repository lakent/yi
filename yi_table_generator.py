#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

shortcode = []
fullcode = []
etymon = []


def fname(arg):
    for x in range(len(etymon)):
        z = etymon[x][0]
        if z == arg:
            return etymon[x][1]
    return ''

def scode(code, index, max_len):

    currentCode = code[0:index]
    
    if currentCode in shortcode and index <= max_len:
        return scode(code, index + 1, max_len)
    elif index > max_len:
        return code 
    else:
        shortcode.append(currentCode)
        return currentCode

def translatesCode(dic, etymon):
    global fullcode
    fullcode = []
    for item in dic:
        s = ''.join([fname(ch) for ch in item[1]])
        new_item = [item[0], s]
        fullcode.append(new_item)
    return fullcode

def readTable(path):
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

def readCharFreq(path):
    char_rank = {}
    try:
        rank = 0
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                l = line.split('\t')
                if l and l[0].strip():
                    character = l[0].strip()
                    char_rank[character] = rank
                    rank += 1
        return char_rank
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return {}

def writeFullTable(path):
    try:
        with open(path, "w", encoding='utf-8') as table_file:
            for i in fullcode:
                character = i[0]
                code = i[1]
                table_file.write(f"{character}\t{code}\n")
    except Exception as e:
        print(f"Error writing full code table: {e}")

def writeShortTable(path, max_len):
    try:
        with open(path, "w", encoding='utf-8') as table_file:
            for i in fullcode:
                character = i[0]
                code = i[1]
                short_code = scode(code, 2, max_len)
                table_file.write(f"{character}\t{short_code}\n")
    except Exception as e:
        print(f"Error writing short code table: {e}")


if __name__ == '__main__':
    
    YI_COMPONENTS_MAPPING_PATH = 'yi_components_mapping.txt'
    YI_SPELLING_PATH = 'yi_spelling.txt'
    CUSTOM_FREQ_PATH = 'char_freq.txt'
    FULLCODE_TABLE_PATH = 'yi_fullcode_table.txt'
    SHORTCODE_TABLE_PATH = 'yi_table.txt'
    
    MAX_SHORTCODE_LENGTH = 6
    
    etymon = readTable(YI_COMPONENTS_MAPPING_PATH)
    print(f"Read components mapping file: {YI_COMPONENTS_MAPPING_PATH}")

    dic = readTable(YI_SPELLING_PATH)
    print(f"Read spelling table file: {YI_SPELLING_PATH}")

    char_rank_map = readCharFreq(CUSTOM_FREQ_PATH)
    
    if not char_rank_map:
        print(f"Warning: Custom frequency map is empty from {CUSTOM_FREQ_PATH}. Sorting will be skipped.")
    else:
        default_rank = len(char_rank_map)

        dic.sort(key=lambda item: char_rank_map.get(item[0], default_rank))
        print(f"Dictionary sorted by custom rank based on {CUSTOM_FREQ_PATH}.")


    fullcode = translatesCode(dic, etymon)
    print("Translated component sequences to full codes.")

    writeFullTable(FULLCODE_TABLE_PATH)
    print("Wrote full code table to " + FULLCODE_TABLE_PATH)

    writeShortTable(SHORTCODE_TABLE_PATH, MAX_SHORTCODE_LENGTH)
    print("Wrote short code table to " + SHORTCODE_TABLE_PATH)