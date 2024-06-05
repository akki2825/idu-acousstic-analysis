"""
Script to convert idu transcription to IPA transcription.
"""
import json

def convert_idu_to_ipa() -> dict:
    """
    Function to convert the IDU transcription to IPA transcription.
    """
    with open('../data/idu_to_ipa.json', 'r', encoding='utf-8-sig') as f:
        idu_to_ipa = json.load(f)

    return idu_to_ipa

if __name__ == '__main__':

    idu_to_ipa = convert_idu_to_ipa()

    with open('../data/roman_to_idu.json') as f:
        roman_to_idu = json.load(f)

    ## exceptions:
    """
    "si": "ʂi",
    "si adrupra": "ʂi adrupra",
    "sibru": "ʂibru",
    "sicu": "ʂicu",
    "si ekombo": "ʂi ekombo",
    "simbra": "ʂimbra",
    "si phu": "ʂi phu",
    """
    roman_to_ipa = {}
    for key in roman_to_idu.keys():
        ipa = []
        for char in roman_to_idu[key]:
            try:
                ipa.append(idu_to_ipa[char])
            except:
                ipa.append(char)
        roman_to_ipa[key] = "".join(ipa)

    ## write the dictionary to a file
    with open('../data/roman_to_ipa.json', 'w') as f:
        json.dump(roman_to_ipa, f, ensure_ascii=False, indent=4)
