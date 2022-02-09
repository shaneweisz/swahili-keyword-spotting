import subprocess
import unittest

from constants.paths import OUTPUT_PATH, SCORING_PATH
from tests.helpers.scorer import get_MTWV_for_ctm_file


class TestMTWVs(unittest.TestCase):
    def test_MTWV_equals_1_for_reference_ctm(self):
        ctm_filename = "reference.ctm"
        output_filename = "test-reference.xml"
        received_mtwv = get_MTWV_for_ctm_file(ctm_filename, output_filename)
        expected_mtwv = 1
        self.assertEqual(expected_mtwv, received_mtwv)

    def test_MTWV_for_onebest_word_ctm(self):
        ctm_filename = "onebest-word.ctm"
        output_filename = "test-onebest-word.xml"
        received_mtwv = get_MTWV_for_ctm_file(ctm_filename, output_filename)
        expected_mtwv = 0.31894
        self.assertEqual(expected_mtwv, received_mtwv)

    def tearDown(self):
        remove_test_output_files()


def remove_test_output_files():
    rm_output_command = f"rm {OUTPUT_PATH}/test-*"
    subprocess.run(rm_output_command, shell=True)

    rm_scoring_command = f"rm -rf {SCORING_PATH}/test-*"
    subprocess.run(rm_scoring_command, shell=True)


if __name__ == "__main__":
    unittest.main()
