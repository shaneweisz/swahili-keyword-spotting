from constants.paths import (
    OUTPUT_PATH,
    SRC_PATH,
    LIB_PATH,
    SCORING_PATH,
    SCRIPTS_PATH,
)


class KWSCommandBuilder:
    def __init__(
        self,
        ctm_filename: str,
        output_filename: str,
        queries_filename: str = "queries-word.xml",
    ):
        self.ctm_filename = ctm_filename
        self.output_filename = output_filename
        self.queries_filename = queries_filename

    def run_kws_command(self) -> str:
        command = "python3 "
        command += f"{SRC_PATH}/kws/main.py "
        command += f"--ctm {self.ctm_filename} "
        command += f"--queries {self.queries_filename} "
        command += f"--output {self.output_filename}"
        return command

    def score_hits_command(self) -> str:
        command = f"{SCRIPTS_PATH}/score.sh {OUTPUT_PATH / self.output_filename} {SCORING_PATH}"  # noqa
        return command

    def get_performance_command(self, iv_or_oov: str = "all") -> str:
        """`iv_or_oov` is either "all", "iv" or "oov"."""
        command = f"{SCRIPTS_PATH}/termselect.sh "
        command += f"{LIB_PATH}/queries/ivoov.map "
        command += f"{OUTPUT_PATH / self.output_filename} "
        command += f"{SCORING_PATH} "
        command += f"{iv_or_oov}"
        return command
