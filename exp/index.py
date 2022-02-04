from collections import defaultdict


class Index:
    @classmethod
    def from_ctm_file(cls, ctm_filename):
        index = cls()
        index.generate_index(ctm_filename)
        return index

    def generate_index(self, ctm_filename: str):
        self.index = defaultdict(list)
        with open(ctm_filename) as ctm_file:
            prev_word_entry = None
            ctm_lines = ctm_file.readlines()

            for ctm_line in ctm_lines:
                word_entry = self.word_entry_from_ctm_line(ctm_line)

                if prev_word_entry:
                    prev_word_entry.next_word_entry = word_entry

                self.add_word_entry_to_index(word_entry)
                prev_word_entry = word_entry

    def word_entry_from_ctm_line(self, ctm_line: str):
        ctm_line = ctm_line.strip("\n")
        kwfile, _, tbeg, dur, token, score = ctm_line.split()
        tbeg, dur, score = float(tbeg), float(dur), float(score)
        word_entry = WordEntry(kwfile, tbeg, dur, token, score, None)
        return word_entry

    def add_word_entry_to_index(self, word_entry):
        self.index[word_entry.word].append(word_entry)

    def get_index(self):
        return self.index

    def search(self, query):
        # TODO
        pass


class WordEntry:
    # The reason we use `class`` here rather than `namedtuple`
    # is because `next_word_entry` key needs to be mutable in the indexing algorithm
    def __init__(self, kw_file, start_time, duration, word, score, next_word_entry):
        self.kw_file = kw_file
        self.start_time = start_time
        self.duration = duration
        self.word = word
        self.score = score
        self.next_word_entry = next_word_entry
