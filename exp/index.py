from collections import defaultdict, namedtuple


class Index:
    TIME_BETWEEN_WORDS_IN_PHRASES = 0.5

    @classmethod
    def from_ctm_file(cls, ctm_filename: str):
        index = cls()
        index.generate_index(ctm_filename)
        return index

    def generate_index(self, ctm_filename: str):
        self.index = defaultdict(list)
        with open(ctm_filename) as ctm_file:
            prev_word_entry = None

            for ctm_line in ctm_file.readlines():
                word_entry = self._word_entry_from_ctm_line(ctm_line)

                if prev_word_entry:
                    prev_word_entry.next_word_entry = word_entry

                self._add_word_entry_to_index(word_entry)

                prev_word_entry = word_entry

    def _word_entry_from_ctm_line(self, ctm_line: str):
        word_entry = WordEntry(*ctm_line.strip("\n").split(), None)
        return word_entry

    def _add_word_entry_to_index(self, word_entry):
        self.index[word_entry.word].append(word_entry)

    def search_for_all_hits(self, query):
        terms = query.split()
        first_term = terms[0]
        first_term_hits = self._get_word_entries_for_word(first_term)
        all_hits = []
        for first_term_hit in first_term_hits:
            query_matched = True
            query_score = first_term_hit.score
            current_word_entry = first_term_hit
            for i in range(1, len(terms)):
                term = terms[i]
                next_word_entry = current_word_entry.next_word_entry

                next_word_matches = term == next_word_entry.word

                words_close_enough = self._words_close_enough(
                    current_word_entry.start_time,
                    current_word_entry.duration,
                    next_word_entry.start_time,
                )

                if next_word_matches and words_close_enough:
                    query_score *= next_word_entry.score
                    current_word_entry = next_word_entry
                    next_word_entry = next_word_entry.next_word_entry
                else:
                    query_matched = False
                    break
            if query_matched:
                last_word_entry = current_word_entry
                all_hits.append(
                    SearchHit(
                        first_term_hit.kw_file,
                        first_term_hit.channel,
                        first_term_hit.start_time,
                        round(
                            last_word_entry.start_time
                            + last_word_entry.duration
                            - first_term_hit.start_time,
                            2,
                        ),
                        query_score,
                    )
                )
        return all_hits

    def _get_word_entries_for_word(self, word):
        return self.index[word]

    def _words_close_enough(
        self, current_word_start_time, current_word_duration, next_word_start_time
    ):
        return (
            next_word_start_time
            <= current_word_start_time
            + current_word_duration
            + self.TIME_BETWEEN_WORDS_IN_PHRASES
        )


class WordEntry:
    # The reason we use `class`` here rather than `namedtuple`
    # is because the value for the `next_word_entry` key
    # needs to be mutable in the indexing algorithm
    def __init__(
        self, kw_file, channel, start_time, duration, word, score, next_word_entry
    ):
        self.kw_file = kw_file
        self.channel = channel
        self.start_time = float(start_time)
        self.duration = float(duration)
        self.word = word.lower()
        self.score = float(score)
        self.next_word_entry = next_word_entry


SearchHit = namedtuple("SearchHit", "kw_file,channel,start_time,duration,score")
