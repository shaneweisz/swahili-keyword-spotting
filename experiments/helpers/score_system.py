from collections import namedtuple
import re
import subprocess
from typing import Tuple
from constants.paths import SCRIPTS_PATH, SCORING_PATH, QUERIES_PATH


MTWVs = namedtuple("MTWVs", "all iv oov threshold")


def get_MTWVs_for_output_file(output_file_path: str) -> MTWVs:
    run_score_command(output_file_path)

    all_mtwv, threshold = run_termselect_command(output_file_path, "all")
    iv_mtwv, _ = run_termselect_command(output_file_path, "iv")
    oov_mtwv, _ = run_termselect_command(output_file_path, "oov")

    return MTWVs(all=all_mtwv, iv=iv_mtwv, oov=oov_mtwv, threshold=threshold)


def run_score_command(output_file_path: str):
    SCORE_COMMAND = f"{SCRIPTS_PATH}/score.sh {output_file_path} {SCORING_PATH}"
    subprocess.run(SCORE_COMMAND, shell=True)


def run_termselect_command(output_file_path: str, iv_oov_tag: str = "all"):
    TERMSELECT_COMMAND = f"{SCRIPTS_PATH}/termselect.sh {QUERIES_PATH}/ivoov.map {output_file_path} {SCORING_PATH} {iv_oov_tag}"  # noqa
    termselect_process = subprocess.run(
        TERMSELECT_COMMAND, shell=True, capture_output=True
    )
    scoring_output = termselect_process.stdout.decode("utf-8")
    mtwv, threshold = extract_MTWV_from_output(scoring_output)
    return mtwv, threshold


def run_termselect_command_for_query_length(
    output_file_path: str, query_length: str = "all"
):
    TERMSELECT_COMMAND = f"{SCRIPTS_PATH}/termselect.sh {QUERIES_PATH}/query-length.map {output_file_path} {SCORING_PATH} {query_length}"  # noqa
    termselect_process = subprocess.run(
        TERMSELECT_COMMAND, shell=True, capture_output=True
    )
    scoring_output = termselect_process.stdout.decode("utf-8")
    mtwv, threshold = extract_MTWV_from_output(scoring_output)
    return mtwv, threshold


def extract_MTWV_from_output(scoring_output: str) -> Tuple[float, float]:
    """
    scoring_output : str
        Example: "all TWV=0.318940153583907 theshold=0.043 number=488\n"
    """
    number_regex = r"\d*\.\d+|\d+"

    twv_text = scoring_output.split()[1]
    mtwv = re.findall(number_regex, twv_text)[0]

    threshold_text = scoring_output.split()[2]
    threshold = re.findall(number_regex, threshold_text)[0]

    return float(mtwv), float(threshold)
