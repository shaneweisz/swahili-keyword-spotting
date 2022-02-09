import re
import subprocess
from tests.helpers.command_builder import KWSCommandBuilder


def get_MTWV_for_ctm_file(ctm_filename: str, output_filename: str) -> float:
    kws_command_builder = KWSCommandBuilder(ctm_filename, output_filename)

    command = kws_command_builder.run_kws_command()
    subprocess.run(command, shell=True)

    command = kws_command_builder.score_hits_command()
    subprocess.run(command, shell=True)

    command = kws_command_builder.get_performance_command()
    process = subprocess.run(command, shell=True, capture_output=True)
    scoring_output = process.stdout.decode("utf-8")
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
