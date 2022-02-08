from constants.paths import CTMS_PATH, DCTS_PATH
from map_words_to_morphs import build_word_to_morphs_dict
from util.file_writer import write_to_file

conversion_dct_file_path = DCTS_PATH / "morph.dct"
original_ctm_file_path = CTMS_PATH / "decode-word.ctm"
new_ctm_file_path = CTMS_PATH / "decode-word-to-morph.ctm"


def main():
    word_to_morphs = build_word_to_morphs_dict(conversion_dct_file_path)
    new_ctm_str = replace_words_with_morphs(original_ctm_file_path, word_to_morphs)
    write_to_file(new_ctm_str, new_ctm_file_path)


def replace_words_with_morphs(original_ctm_file_path, word_to_morphs):
    with open(original_ctm_file_path) as original_ctm_file:
        lines = original_ctm_file.readlines()

    new_ctm_str = ""
    for line in lines:
        file, channel, tbeg, dur, word, score = line.strip().split()
        channel, tbeg, dur, score = int(channel), float(tbeg), float(dur), float(score)
        morphs = word_to_morphs[word].split()

        morph_dur = dur / len(morphs)
        morph_tbeg = tbeg
        morph_score = score ** (1 / len(morphs))

        for morph in morphs:
            new_line = f"{file} {channel} {morph_tbeg:.2f} {morph_dur:.2f} {morph} {morph_score:.6f}\n"  # noqa
            new_ctm_str += new_line
            morph_tbeg += morph_dur

    return new_ctm_str


if __name__ == "__main__":
    main()
