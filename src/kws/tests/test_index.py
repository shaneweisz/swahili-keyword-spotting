import unittest
from index import Index

test_ctm_file_path = "/homes/sw984/MLMI14/lib/ctms/reference.ctm"

# First 5 lines of file:
"""
BABEL_OP2_202_10524_20131009_200043_inLine 1 3.77 0.340 halo 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 6.30 0.340 halo 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 6.64 0.370 habari 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 7.01 0.690 ya 1.0000
BABEL_OP2_202_10524_20131009_200043_inLine 1 9.02 0.580 mkubwa 1.0000
"""


class TestIndexer(unittest.TestCase):
    index = Index.from_ctm(test_ctm_file_path)
    first_habari_entry = index.index["habari"][0]

    def test_duration_stored(self):
        self.assertEqual(self.first_habari_entry.duration, 0.37)

    def test_next_word(self):
        next_word_entry = self.first_habari_entry.next_word_entry
        self.assertEqual(next_word_entry.word, "ya")

    def test_next_word_of_next_word(self):
        next_word_entry = self.first_habari_entry.next_word_entry
        self.assertEqual(next_word_entry.next_word_entry.word, "mkubwa")


if __name__ == "__main__":
    unittest.main()
