from collections import defaultdict
import argparse


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--ctm", type=str, help="The path to the input CTM file", required=True
    )

    args = arg_parser.parse_args()
    ctm_file = args.ctm

    index = Index(ctm_file)

    index.build()

    print(index.index.keys())


class WordOccurrence:
    def __init__(self, word, file, start_time, duration, score, next_word):
        self.word = word
        self.file = file
        self.start_time = start_time
        self.duration = duration
        self.score = score
        self.next_word = next_word


class Index:
    def __init__(self, ctm_file):
        self.index = defaultdict(list)
        self.ctm_file = ctm_file

    def build(self):
        with open(self.ctm_file) as asr_file:
            prev_word_occurrence = None
            for line in asr_file.readlines():
                line = line.strip("\n")
                file, _, start_time, duration, word, score = line.split()
                start_time = float(start_time)
                duration = float(duration)
                score = float(score)

                word_occurence = WordOccurrence(
                    word, file, start_time, duration, score, None
                )

                if prev_word_occurrence:
                    st = prev_word_occurrence.start_time
                    dur = prev_word_occurrence.duration
                    et = st + dur
                    if start_time <= et + 0.5:
                        prev_word_occurrence.next_word = word_occurence

                self.index[word].append(word_occurence)
                prev_word_occurrence = word_occurence

    def search(self, query):
        pass

    def __str__(self):
        return "I am an Index object"


if __name__ == "__main__":
    main()
