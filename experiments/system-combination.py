import argparse
from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file
from combine_systems import combine_sets_of_hits
from set_of_hits import SetOfHits


methods = ["CombSUM", "CombMNZ", "WCombMNZ"]

RESULTS_HEADER = "System,All,IV,OOV"


def main(experiment_name, systems_sets):
    results_file = setup_results_file(experiment_name)

    for systems, weights in systems_sets:
        sets_of_hits = [
            SetOfHits.from_XML(OUTPUT_PATH / f"{system}.xml") for system in systems
        ]

        for method in methods:
            combined_set_of_hits = combine_sets_of_hits(sets_of_hits, method, weights)

            output_file_name = "_+_".join(systems) + "_" + method + ".xml"
            output_file_path = OUTPUT_PATH / "system-combination" / output_file_name
            combined_set_of_hits.write_hits_to_file(output_file_path)
            mtwvs = get_MTWVs_for_output_file(output_file_path)
            line = get_results_line(mtwvs, output_file_name)
            write_line_to_file(results_file, line)

            normalised_output_file_path = normalise(output_file_path, gamma=1)
            mtwvs = get_MTWVs_for_output_file(normalised_output_file_path)
            line = get_results_line(mtwvs, normalised_output_file_path.name)
            write_line_to_file(results_file, line)

    cleanup_results_file(results_file)


def normalise(output_file_path, gamma):
    set_of_hits = SetOfHits.from_XML(output_file_path)
    set_of_hits.normalise_scores(gamma)

    normalised_output_file_name = output_file_path.name.strip(".xml") + "-STO.xml"
    normalised_output_file_path = output_file_path.parent / normalised_output_file_name
    set_of_hits.write_hits_to_file(normalised_output_file_path)

    return normalised_output_file_path


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


def get_results_line(mtwvs: MTWVs, system: str):
    line = f"{system},{mtwvs.all:.3f},{mtwvs.iv:.3f},{mtwvs.oov:.3f}"
    return line


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
        experiment_name = "system-combination-lattice"
        systems_sets = [
            (["lattice-morph", "lattice-word"], [0.36, 0.399]),
            (["STO-lattice-morph", "STO-lattice-word"], [0.52, 0.46]),
            (["lattice-morph", "lattice-word-sys2"], [0.36, 0.403]),
            (["STO-lattice-morph", "STO-lattice-word-sys2"], [0.52, 0.465]),
            (
                ["lattice-word", "lattice-morph", "lattice-word-sys2"],
                [0.399, 0.36, 0.403],
            ),
            (
                ["STO-lattice-word", "STO-lattice-morph", "STO-lattice-word-sys2"],
                [0.46, 0.52, 0.465],
            ),
        ]
    elif args.asr_type == "onebest":
        experiment_name = "system-combination-onebest"
        systems_sets = [
            (["onebest-word", "onebest-morph"], [0.319, 0.318]),
            (["STO-onebest-word", "STO-onebest-morph"], [0.32, 0.326]),
        ]

    main(experiment_name, systems_sets)
