from typing import Dict
from bs4 import BeautifulSoup
from constants.paths import DCTS_PATH, QUERIES_PATH
from util.file_writer import write_to_file
from map_words_to_morphs import build_word_to_morphs_dict

conversion_dct_file_path = DCTS_PATH / "morph.kwslist.dct"
original_queries_file_path = QUERIES_PATH / "queries.xml"
new_queries_file_path = QUERIES_PATH / "queries-morph.xml"


def main():
    word_to_morphs = build_word_to_morphs_dict(conversion_dct_file_path)
    xml_str = get_xml_str_from_queries_file(original_queries_file_path)
    new_xml_str = replace_words_with_morphs(xml_str, word_to_morphs)
    write_to_file(new_xml_str, new_queries_file_path)


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


def decompose_phrase_into_morphs(phrase, word_to_morphs: Dict[str, str]):
    return " ".join([word_to_morphs[word] for word in phrase.split()])


if __name__ == "__main__":
    main()
