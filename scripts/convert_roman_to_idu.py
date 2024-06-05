"""
Script to convert the Roman transcription to the IDU transcription.
"""
import json
import unicodedata

def strip_accents(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

def convert_roman_to_idu() -> dict:
    """
    Function to convert the Roman transcription to IDU transcription.
    """

    with open('../data/idu_mishmi_dictionary/Script/simplified_idu_eng_dict.json') as f:
        roman_to_idu = json.load(f)

    ## strip the accent markers
    roman_to_idu_simplified = {key: strip_accents(value) for key, value in roman_to_idu.items()}

    for key in list(roman_to_idu_simplified.keys()):
        if ',' in key:
            keys = key.split(',')
            values = roman_to_idu_simplified[key].split(',')
            for k, v in zip(keys, values):
                roman_to_idu_simplified[k] = v
            del roman_to_idu_simplified[key]
    return roman_to_idu_simplified

if __name__ == '__main__':
    roman_to_idu = convert_roman_to_idu()
    ## write the dictionary to a file
    with open('../data/roman_to_idu.json', 'w+') as f:
        json.dump(roman_to_idu, f, ensure_ascii=False, indent=4)
