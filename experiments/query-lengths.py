from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import run_termselect_command_for_query_length

RESULTS_HEADER = "System,QueryLength,MTWV,Threshold"


output_file_paths = [
    OUTPUT_PATH / "lattice-morph.xml",
    OUTPUT_PATH / "STO-lattice-morph.xml",
    OUTPUT_PATH
    / "system-combination"
    / "STO-lattice-word_+_STO-lattice-morph_+_STO-lattice-word-sys2_WCombMNZ-STO.xml",
]


def main():
    experiment_name = "query-lengths"
    results_file = setup_results_file(experiment_name)

    for output_file_path in output_file_paths:
        for query_length in range(1, 6):
            mtwv, threshold = run_termselect_command_for_query_length(
                output_file_path, query_length
            )
            line = f"{output_file_path.name},{query_length},{mtwv:.3f},{threshold:.3f}"
            write_line_to_file(results_file, line)

    cleanup_results_file(results_file)


def setup_results_file(experiment_name: str):
    results_file_path = RESULTS_PATH / f"{experiment_name}.csv"
    results_file = open(results_file_path, "w")
    write_line_to_file(results_file, RESULTS_HEADER)
    return results_file


def write_line_to_file(file, line):
    file.write(line + "\n")
    file.flush()


def cleanup_results_file(file):
    file.close()


if __name__ == "__main__":
    main()
