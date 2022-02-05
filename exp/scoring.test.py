import subprocess
import unittest
from pathlib import Path


BASE_PATH = Path("/homes/sw984/MLMI14/")
LIB_PATH = BASE_PATH / "lib"
EXP_PATH = BASE_PATH / "exp"
SCRIPTS_PATH = BASE_PATH / "scripts"
OUTPUT_PATH = BASE_PATH / "output"
SCORING_PATH = BASE_PATH / "hits"


class KWSCommandBuilder:
    def __init__(
        self,
        ctm_filename: str,
        output_filename: str,
        queries_filename: str = "queries.xml",
    ):
        self.ctm_filename = ctm_filename
        self.output_filename = output_filename
        self.queries_filename = queries_filename

    def run_kws_command(self) -> str:
        command = "python3 "
        command += f"{EXP_PATH}/main.py "
        command += f"--ctm_file {LIB_PATH}/ctms/{self.ctm_filename} "
        command += f"--queries {LIB_PATH}/kws/{self.queries_filename} "
        command += f"--output_filename {OUTPUT_PATH}/{self.output_filename}"
        return command

    def score_hits_command(self) -> str:
        command = f"{SCRIPTS_PATH}/score.sh "
        command += f"{OUTPUT_PATH}/{self.output_filename} "
        command += f"{SCORING_PATH}"
        return command

    def get_performance_command(self, iv_or_oov: str = "all") -> str:
        """`iv_or_oov` is either "all", "iv" or "oov"."""
        command = f"{SCRIPTS_PATH}/termselect.sh "
        command += f"{LIB_PATH}/terms/ivoov.map "
        command += f"{OUTPUT_PATH}/{self.output_filename} "
        command += f"{SCORING_PATH} "
        command += f"{iv_or_oov}"
        return command


class TestKwsScores(unittest.TestCase):
    def testKwsOnReference(self):
        asr_to_test = "reference"
        received_output = score_system(asr_to_test)
        expected_output = 1
        self.assertEqual(expected_output, received_output)

    def testKwsOnDecode(self):
        asr_to_test = "decode"
        received_output = score_system(asr_to_test)
        expected_output = 0.31894
        self.assertEqual(expected_output, received_output)

    def tearDown(self):
        remove_test_scoring()


def score_system(asr_to_test: str) -> float:
    ctm_filename = f"{asr_to_test}.ctm"
    output_filename = f"test-{asr_to_test}.xml"

    kws_command_builder = KWSCommandBuilder(ctm_filename, output_filename)
    subprocess.run(kws_command_builder.run_kws_command(), shell=True)

    remove_test_scoring()
    subprocess.run(kws_command_builder.score_hits_command(), shell=True)

    process = subprocess.run(
        kws_command_builder.get_performance_command(), shell=True, capture_output=True
    )

    score_output = process.stdout.decode("utf-8")
    twv = get_TWV(score_output)

    return twv


def remove_test_scoring():
    subprocess.run(f"rm -rf {SCORING_PATH}/test*", shell=True)


def get_TWV(score_output: str) -> float:
    """An example of `score_output` is
    "all TWV=0.318940153583907 theshold=0.043 number=488\n"
    """
    index_of_twv = score_output.find("TWV=") + len("TWV=")
    twv = score_output[index_of_twv : score_output.find(" ", index_of_twv)]
    twv = round(float(twv), 5)
    return twv


if __name__ == "__main__":
    unittest.main()
