import subprocess
from command_builder import KWSCommandBuilder


def get_TWV_for_ctm_file(ctm_filename: str, output_filename: str) -> float:
    kws_command_builder = KWSCommandBuilder(ctm_filename, output_filename)

    command = kws_command_builder.run_kws_command()
    subprocess.run(command, shell=True)

    command = kws_command_builder.score_hits_command()
    subprocess.run(command, shell=True)

    command = kws_command_builder.get_performance_command()
    process = subprocess.run(command, shell=True, capture_output=True)
    scoring_output = process.stdout.decode("utf-8")
    twv = extract_TWV(scoring_output)

    return twv


def extract_TWV(scoring_output: str) -> float:
    """An example of `scoring_output` is
    "all TWV=0.318940153583907 theshold=0.043 number=488\n"
    """
    index_of_twv = scoring_output.find("TWV=") + len("TWV=")
    twv = scoring_output[index_of_twv : scoring_output.find(" ", index_of_twv)]
    twv = round(float(twv), 5)
    return twv
