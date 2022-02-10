from collections import namedtuple
import re
import subprocess
from constants.paths import SCRIPTS_PATH, SCORING_PATH, QUERIES_PATH


MTWVs = namedtuple("MTWVs", "all iv oov")


def get_MTWVs_for_output_file(output_file_path: str) -> MTWVs:
    run_score_command(output_file_path)

    all_mtwv = run_termselect_command(output_file_path, "all")
    iv_mtwv = run_termselect_command(output_file_path, "iv")
    oov_mtwv = run_termselect_command(output_file_path, "oov")

    return MTWVs(all=all_mtwv, iv=iv_mtwv, oov=oov_mtwv)


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


def extract_MTWV_from_output(scoring_output: str) -> float:
    """
    scoring_output : str
        Example: "all TWV=0.318940153583907 theshold=0.043 number=488\n"
    """
    number_regex = r"\d*\.\d+|\d+"
    mtwv, _, _ = re.findall(number_regex, scoring_output)
    return float(mtwv)
