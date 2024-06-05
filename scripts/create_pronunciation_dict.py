from typing import List
import epitran.vector
import pandas as pd
from tqdm.auto import tqdm

tqdm.pandas()


def transcribe_word(word: str) -> List[str]:
    """Transcribe a word to segments using epitran."""
    transcriptions = epi.word_to_segs(word)
    ipa = [tuples[3] for tuples in transcriptions]
    return ipa


def clean_word(word: str) -> str:
    """Clean the word to remove punctuation."""
    cleaned_word = []
    for character in word:
        if character.isalpha():
            cleaned_word.append(character)
    word = "".join(cleaned_word)
    return word


def generate_dict_entry(wordlist: List[str]) -> None:
    """Get the ipa representation of the transcriptions."""
    pronunciation_dict = {}
    for word in word_list:
        if word in pronunciation_dict:
            continue
        word = clean_word(word)
        ipa = transcribe_word(word)
        pronunciation_dict[word] = ipa
    return pronunciation_dict

if __name__ == "__main__":
    epi = epitran.vector.VectorsWithIPASpace("Kin-Latn", ["Kin-Latn"])

    with open("../data/wordlist.txt") as f:
        words = f.readlines()
        words = [item.strip() for item in words]


    words_ipa = generate_dict_entry(words)

    with open("../data/idu_generated_pronunciation_dict.txt", "w+") as f:
        for key, value in all_pronunciations.items():
            if value and value != [""]:
                f.write("%s\t%s\n" % (key, " ".join(value)))
