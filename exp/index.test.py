import unittest
from index import Index

test_ctm_filename = "/homes/sw984/MLMI14/lib/ctms/reference.ctm"

# First 5 lines of file:
"""
BABEL_OP2_202_10524_20131009_200043_inLine 1 3.77 0.340 halo 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 6.30 0.340 halo 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 6.64 0.370 habari 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 7.01 0.690 ya 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 9.02 0.580 mkubwa 1.0000
"""


class TestIndexer(unittest.TestCase):
    index = Index.from_ctm_file(test_ctm_filename)
    first_habari_entry = index.get_index()["habari"][0]

    def test_duration_stored(self):
        self.assertEquals(self.first_habari_entry.duration, 0.37)

    def test_next_word(self):
        next_word_entry = self.first_habari_entry.next_word_entry
        self.assertEquals(next_word_entry.word, "ya")

    def test_next_word_of_next_word(self):
        next_word_entry = self.first_habari_entry.next_word_entry
        self.assertEquals(next_word_entry.next_word_entry.word, "mkubwa")


if __name__ == "__main__":
    unittest.main()
