from pathlib import Path
from bs4 import BeautifulSoup


def decompose_phrase_into_morphs(phrase: str):
    return " ".join([word_to_morphs[word] for word in phrase.split()])


BASE_PATH = Path("/homes/sw984/MLMI14/")
DCTS_PATH = BASE_PATH / "morph-decomposition" / "dcts"
QUERIES_PATH = BASE_PATH / "queries"

queries_dct_file_path = DCTS_PATH / "morph.kwslist.dct"
with open(queries_dct_file_path) as queries_dct_file:
    word_morphs_pairs = [
        line.strip().split(maxsplit=1) for line in queries_dct_file.readlines()
    ]
    word_to_morphs = {word: morphs for [word, morphs] in word_morphs_pairs}


queries_file_path = QUERIES_PATH / "queries.xml"
with open(queries_file_path) as queries_file:
    xml = queries_file.read()

soup = BeautifulSoup(xml)
keyword_list = soup.find_all("kw")
for keyword in keyword_list:
    id = keyword.get("kwid")
    text = keyword.kwtext.text.lower()
    keyword.kwtext.string = decompose_phrase_into_morphs(text)

with open(QUERIES_PATH / "queries-morph.xml", "w") as decomposed_queries_file:
    decomposed_queries_file.write(soup.prettify())
