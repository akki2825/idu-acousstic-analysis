"""
Script to convert English-Idu filenames to English-IPA filenames.

Original: Active__Aamonyi-Active__Aambrobro.wav
Converted: Active__IPA-Active__IPA.wav

Usage:
    convert_filenames_to_ipa.py --type-recording=<tr>

Options:
    --type-recording=<tr>   Type of recording (nasal or non_nasal)
"""
from docopt import docopt
import os
import json
from fuzzywuzzy import fuzz, process

### function to get fuzzy match using levenstein distance
def get_fuzzy_match(word: str, word_list: list) -> str:
    """
    Function to get the fuzzy match of a word in a list of words.
    """
    match = process.extractOne(word, word_list, scorer=fuzz.ratio)
    return match[0]

def convert_filenames_to_ipa(type_recording: str) -> None:
    """
    Function to convert English-Idu filenames to English-IPA filenames.
    """
    with open('../data/roman_to_ipa.json', 'r', encoding='utf-8-sig') as f:
        roman_to_ipa = json.load(f)

    # convert key and value to lowercase
    roman_to_ipa = {key.lower(): value.lower() for key, value in roman_to_ipa.items()}
    with open('../data/roman_to_idu.json', 'r', encoding='utf-8-sig') as f:
        roman_to_idu = json.load(f)

    roman_to_idu = {key.lower(): value.lower() for key, value in roman_to_idu.items()}
    ## merge roman_to_ipa and roman_to_idu with same keys
    idu_to_ipa = {value: roman_to_ipa[key] for key, value in roman_to_idu.items()}
    ## if there are commas in the keys, split them and map them to the values with commas
    for key in list(idu_to_ipa.keys()):
        if ',' in key:
            keys = key.split(',')
            values = idu_to_ipa[key].split(',')
            for k, v in zip(keys, values):
                idu_to_ipa[k] = v
            del idu_to_ipa[key]
    ## write idu_to_ipa to a json file
    with open('../data/idu_to_ipa.json', 'w+') as f:
        json.dump(idu_to_ipa, f, ensure_ascii=False, indent=4)
    ## read filenames from the directory
    for filename in os.listdir('../data/' + type_recording + '_recordings/'):
        print(filename)
        if filename.endswith('.wav'):
            ## split the filename
            new_filename = filename.lower()
            name = new_filename.split('__')
            idu_name = name[1].split('.')[0]
            english_name = name[0]
            try:
                idu_ipa = idu_to_ipa[idu_name]
                os.rename('../data/' + type_recording + '_recordings/' + filename, '../data/' + type_recording + '_ipa_recordings/' + english_name + "_" + idu_ipa + '.wav')
            except:
                idu_name = get_fuzzy_match(idu_name, list(idu_to_ipa.keys()))
                idu_ipa = idu_to_ipa[idu_name]

                with open('../data/fuzzy_' + type_recording + '.txt', 'a') as f:
                    f.write(idu_name + " " + idu_ipa + '\n')

                os.rename('../data/' + type_recording + '_recordings/' + filename, '../data/' + type_recording + '_fuzzy_ipa_recordings/' + english_name + "_" + idu_ipa + '.wav')

                with open('../data/missing_' + type_recording + '.txt', 'a') as f:
                    f.write(filename + '\n')

if __name__ == '__main__':
    args = docopt(__doc__)
    type_recording = args['--type-recording']
    convert_filenames_to_ipa(type_recording)
