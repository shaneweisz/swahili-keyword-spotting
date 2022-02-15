import argparse
from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file


RESULTS_HEADER = "File,All,IV,OOV"


def main(experiment_name, output_file_names):
    results_file = setup_results_file(experiment_name)

    for output_file_name in output_file_names:
        mtwvs = get_MTWVs_for_output_file(OUTPUT_PATH / output_file_name)
        line = get_results_line(mtwvs, output_file_name)
        write_line_to_file(results_file, line)

    cleanup_results_file(results_file)


def setup_results_file(experiment_name: str):
    results_file_path = RESULTS_PATH / f"{experiment_name}.csv"
    results_file = open(results_file_path, "w")
    write_line_to_file(results_file, RESULTS_HEADER)
    return results_file


def get_results_line(mtwvs: MTWVs, output_file_name: str):
    line = f"{output_file_name},{mtwvs.all:.3f},{mtwvs.iv:.3f},{mtwvs.oov:.3f}"
    return line


def write_line_to_file(file, line):
    file.write(line + "\n")
    file.flush()


def cleanup_results_file(file):
    file.close()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--asr_type",
        type=str,
        help="`lattice` or `onebest`",
        required=True,
    )

    args = arg_parser.parse_args()

    if args.asr_type == "lattice":
        experiment_name = "lattice-kws"
        output_file_names = [
            "lattice-word.xml",
            "lattice-morph.xml",
            "lattice-word-sys2.xml",
            "STO-lattice-word.xml",
            "STO-lattice-morph.xml",
            "STO-lattice-word-sys2.xml",
        ]
    elif args.asr_type == "onebest":
        experiment_name = "onebest-kws"
        output_file_names = [
            "reference.xml",
            "onebest-word.xml",
            "onebest-morph.xml",
            "onebest-word-to-morph.xml",
            "STO-reference.xml",
            "STO-onebest-word.xml",
            "STO-onebest-morph.xml",
            "STO-onebest-word-to-morph.xml",
        ]

    main(experiment_name, output_file_names)
