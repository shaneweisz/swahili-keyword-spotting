from typing import Dict
from bs4 import BeautifulSoup
from constants.paths import DCTS_PATH, QUERIES_PATH


def main(queries_dct_file_path, queries_file_path):
    word_to_morphs = build_word_to_morphs_dict(queries_dct_file_path)
    xml_str = get_xml_str_from_queries_file(queries_file_path)
    new_xml_str = replace_words_with_morphs(xml_str, word_to_morphs)
    output_new_queries_file(new_xml_str)


def build_word_to_morphs_dict(dct_file_path):
    with open(dct_file_path) as queries_dct_file:
        word_morphs_pairs = [
            line.strip().split(maxsplit=1) for line in queries_dct_file.readlines()
        ]

    word_to_morphs = {word: morphs for [word, morphs] in word_morphs_pairs}

    return word_to_morphs


def get_xml_str_from_queries_file(queries_file_path):
    with open(queries_file_path) as queries_file:
        xml_str = queries_file.read()
    return xml_str


def replace_words_with_morphs(xml_str, word_to_morphs):
    soup = BeautifulSoup(xml_str, "xml")
    keyword_list = soup.find_all("kw")
    for keyword in keyword_list:
        phrase = keyword.kwtext.text.lower()
        keyword.kwtext.string = decompose_phrase_into_morphs(phrase, word_to_morphs)
    new_xml_str = soup.prettify()
    return new_xml_str


def output_new_queries_file(new_xml_str):
    with open(QUERIES_PATH / "queries-morph.xml", "w") as decomposed_queries_file:
        decomposed_queries_file.write(new_xml_str)


def decompose_phrase_into_morphs(phrase, word_to_morphs: Dict[str, str]):
    return " ".join([word_to_morphs[word] for word in phrase.split()])


if __name__ == "__main__":
    queries_dct_file_path = DCTS_PATH / "morph.kwslist.dct"
    queries_file_path = QUERIES_PATH / "queries.xml"
    main(queries_dct_file_path, queries_file_path)