def build_word_to_morphs_dict(conversion_dct_file_path):
    with open(conversion_dct_file_path) as conversion_dct_file:
        word_morphs_pairs = [
            line.strip().split(maxsplit=1) for line in conversion_dct_file.readlines()
        ]

    word_to_morphs = {word: morphs for [word, morphs] in word_morphs_pairs}

    return word_to_morphs
