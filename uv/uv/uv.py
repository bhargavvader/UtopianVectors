import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
import spacy

SEARCH_WORDS = ['justice', 'man', 'woman', 'artificial_intelligence', 'factory', 'labor', 'state',
                'economy', 'food', 'freedom', 'health', 'time', 'home', 'house', 'government', 'immigrant',
                'safety', 'police', 'policing', 'crime', 'equality', 'planet', 'planetary', 'atmosphere','space', 'earth', 'diamond', 
                'technology', 'machinery', 'machine', 'cyber', 'computer', 'digital', 'industrial', 'future', 'automation',
                'robot', 'science', 'network', 'current', 'interface', 'virtual', 'military', 'engineer', 'system']

#possible additions: mars

def lemmatize_search_words():
    '''
    lemmatize serach words to compare to our lemmatized corpus
    code to lemmatize individual words using spacy taken from this post: https://stackoverflow.com/questions/59636002/spacy-lemmatization-of-a-single-word
    for this function to work you need to download the spacy english vocabulary using 'python -m spacy download en_core_web_sm'
    '''

    lemm_search_words = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) # just keep tagger for lemmatization

    for word in SEARCH_WORDS:
        lemm_search_words.append(" ".join([token.lemma_ for token in nlp(word)]))

    return list(dict.fromkeys(lemm_search_words)) #return list with duplicates removed

def load_clean_metadata():
    
    with open('../metadata/eutopia_metadata_clean.txt', 'rb') as f:
        book_info_eutopia = pkl.load(f) 

    with open('../metadata/dystopia_metadata_clean.txt', 'rb') as f:
        book_info_dystopia = pkl.load(f)

    return book_info_eutopia, book_info_dystopia

def get_text_dicts():

    print('note: does not include scanned pdfs')

    with open('../../Cleaned-Data/cleaned_texts_pdf.json') as json_file:
        cleaned_texts_pdf = json.load(json_file)
    with open('../../Cleaned-Data/cleaned_texts_epub_txt.json') as json_file:
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

def get_lemmatized_eutopia_text_dicts():

    print('note: does not include scanned pdfs')

    with open('../../Cleaned-Data/lemmatized_books.json') as json_file:
        cleaned_texts = json.load(json_file)

    cln_txts_eu_dict = {}

    #the keys in our input json files are file names with extensions. 
    #remove extensions so that the dictionary keys match the IDs in the metadata table.
    for key, val in cleaned_texts.items():
        new_key = key.split('.')[0]
        if "scanned" not in new_key:
            cln_txts_eu_dict[new_key] = val

    return cln_txts_eu_dict

def get_all_texts(text_dict, book_info=None, exclude_rejects = True):

    if exclude_rejects:
        mask =  ~book_info.fillna('0').jode_notes.str.contains("reject_list")
        ids = book_info[mask].ID.values 
        return [text_dict[key] for key in ids if key in text_dict]

    else:
        return [text for text in text_dict.values()]
    

def get_texts_year_range(year_range_lo, year_range_hi, book_info, text_dict, exclude_rejects = True):
    
    if exclude_rejects:
        mask = (book_info.year > year_range_lo) & (book_info.year <= year_range_hi) & (~book_info.fillna('0').jode_notes.str.contains("reject_list"))
    else:
        mask = (book_info.year > year_range_lo) & (book_info.year <= year_range_hi)
    ids = book_info[mask].ID.values
    texts = [text_dict[key] for key in ids if key in text_dict]
    
    print('texts in date range: ' + str(len(texts)))
    return texts

def get_texts_w_keyword(kw, book_info, text_dict, exclude_rejects = True):
    
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

    if exclude_rejects:
        mask = book_info.fillna('0').keywords.str.contains(kw) & (~book_info.fillna('0').jode_notes.str.contains("reject_list"))
    else:
        mask = book_info.fillna('0').keywords.str.contains(kw)    
    ids = book_info[mask].ID.values
    texts = [text_dict[key] for key in ids if key in text_dict]

    print('texts with keyword ' + kw + ': ' + str(len(texts)))
    return texts


