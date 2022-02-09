import re
import subprocess
from constants.paths import SCRIPTS_PATH, SCORING_PATH, QUERIES_PATH


def get_MTWV_for_output_file(output_file_path: str) -> float:
    run_score_command(output_file_path)
    mtwv = run_termselect_command(output_file_path)
    return mtwv


def run_score_command(output_file_path: str):
    SCORE_COMMAND = f"{SCRIPTS_PATH}/score.sh {output_file_path} {SCORING_PATH}"
    subprocess.run(SCORE_COMMAND, shell=True)


def run_termselect_command(output_file_path: str, iv_oov_tag: str = "all"):
    TERMSELECT_COMMAND = f"{SCRIPTS_PATH}/termselect.sh {QUERIES_PATH}/ivoov.map {output_file_path} {SCORING_PATH} {iv_oov_tag}"  # noqa
    termselect_process = subprocess.run(
        TERMSELECT_COMMAND, shell=True, capture_output=True
    )
    scoring_output = termselect_process.stdout.decode("utf-8")
    mtwv = extract_MTWV_from_output(scoring_output)
    return mtwv


def extract_MTWV_from_output(scoring_output: str, ndigits: int = 5) -> float:
    """
    scoring_output : str
        Example: "all TWV=0.318940153583907 theshold=0.043 number=488\n"
    """
    number_regex = r"\d*\.\d+|\d+"
    mtwv, _, _ = re.findall(number_regex, scoring_output)
    mtwv = round(float(mtwv), ndigits)
    return mtwv
