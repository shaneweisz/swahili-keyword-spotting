import subprocess
import unittest

from constants.paths import OUTPUT_PATH, SCORING_PATH
from scorer import get_TWV_for_ctm_file


class TestKwsTWVs(unittest.TestCase):
    def test_kws_twv_on_reference(self):
        ctm_filename = "reference.ctm"
        output_filename = "test-reference.xml"
        received_twv = get_TWV_for_ctm_file(ctm_filename, output_filename)
        expected_twv = 1
        self.assertEqual(expected_twv, received_twv)

    def test_kws_twv_on_decode(self):
        ctm_filename = "decode.ctm"
        output_filename = "test-decode.xml"
        received_twv = get_TWV_for_ctm_file(ctm_filename, output_filename)
        expected_twv = 0.31894
        self.assertEqual(expected_twv, received_twv)

    def tearDown(self):
        remove_test_output_files()


def remove_test_output_files():
    rm_output_command = f"rm {OUTPUT_PATH}/test-*"
    subprocess.run(rm_output_command, shell=True)

    rm_scoring_command = f"rm -rf {SCORING_PATH}/test-*"
    subprocess.run(rm_scoring_command, shell=True)


if __name__ == "__main__":
    unittest.main()
