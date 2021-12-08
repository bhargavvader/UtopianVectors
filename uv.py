import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl

SEARCH_WORDS = ['justice', 'man', 'woman', 'artificial_intelligence', 'factory', 'labour', 'state',
                'economy', 'food', 'freedom', 'health', 'time', 'home', 'house', 'government', 'immigrant',
                'safety', 'police', 'policing', 'crime', 'equality', 'planet', 'space', 'earth']

def load_clean_metadata():
    
    with open('eutopia_metadata_clean.txt', 'rb') as f:
        book_info_eutopia = pkl.load(f) 

    with open('dystopia_metadata_clean.txt', 'rb') as f:
        book_info_dystopia = pkl.load(f)

    return book_info_eutopia, book_info_dystopia

def get_text_dicts():

    print('note: does not include scanned pdfs')

    with open('../Cleaned-Data/cleaned_texts_pdf.json') as json_file:
        cleaned_texts_pdf = json.load(json_file)
    with open('../Cleaned-Data/cleaned_texts_epub_txt.json') as json_file:
        cleaned_texts_epub_txt = json.load(json_file)

    cln_txts_eu_dict = {}

    #the keys in our input json files are file names with extensions. 
    #remove extensions so that the dictionary keys match the IDs in the metadata table.
    for key, val in cleaned_texts_pdf.items():
        new_key = key.split('.')[0]
        if "scanned" not in new_key:
            cln_txts_eu_dict[new_key] = val
    for key, val in cleaned_texts_epub_txt.items():
        new_key = key.split('.')[0]
        if "scanned" not in new_key:
            cln_txts_eu_dict[new_key] = val

    with open('../Cleaned-Data/cleaned_texts_dystopia.json') as json_file:
        cleaned_texts_dystopia = json.load(json_file)
    
    cln_txts_dys_dict = {}
    
    for key, val in cleaned_texts_dystopia.items():
        new_key = key.split('.')[0]
        if "scanned" not in new_key:
            cln_txts_dys_dict[key.split('.')[0]] = val

    return cln_txts_eu_dict, cln_txts_dys_dict

def get_all_texts(text_dict):

    return [text for text in text_dict.values()]
    

def get_texts_year_range(year_range_lo, year_range_hi, book_info, text_dict):
    
    ids = book_info[(book_info.year > year_range_lo) & (book_info.year <= year_range_hi)].ID.values
    texts = [text_dict[key] for key in ids if key in text_dict]
    
    print('texts in date range: ' + str(len(texts)))
    return texts

def get_texts_w_keyword(kw, book_info, text_dict):
    
    possible_keywords = ['Aotearoa/New Zealand author', 'Female author', 'English author', 'Irish author', 
     'Male author', 'African author', 'Transgender author', 'US author', 'UK author', 
     'Canadian author', 'Latinx author', 'African American author', 'Cuban-American author',
     'Scottish author', 'Indian author', 'French author', 'Australian author', 
     'Czech author', 'Northern Ireland author', 'Israeli author', 'Nigerian author', 
     'South African author', 'Iranian author', 'Botswanan author', 'Armenian author', 
     'Italian author', 'German author', 'Welsh author', 'Slovenian author']
        
    if kw not in possible_keywords:
        print('no texts labeled with that keyword. possible keywords are:')
        print(possible_keywords)

    bi_no_na = book_info[~book_info.keywords.isna()]
    ids = bi_no_na[bi_no_na.keywords.str.contains(kw)].ID.values
    texts = [text_dict[key] for key in ids if key in text_dict]

    print('texts with keyword ' + kw + ': ' + str(len(texts)))
    return texts


