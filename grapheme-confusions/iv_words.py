from constants.paths import CTMS_PATH

word_ctm_file_path = CTMS_PATH / "onebest-word.ctm"


def get_iv_words():
    iv_words = set()
    with open(word_ctm_file_path) as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip("\n")
        tokens = line.split()
        iv_word = tokens[-2]
        iv_words.add(iv_word)
    return iv_words
