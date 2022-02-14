from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file
from combine_systems import combine_sets_of_hits
from set_of_hits import SetOfHits

experiment_name = "onebest-system-combination"

systems_sets = [
    ["onebest-word", "onebest-morph"],
    ["onebest-word", "onebest-morph", "onebest-word-to-morph"],
]

RESULTS_HEADER = "file,all,iv,oov"


def main():
    results_file = setup_results_file(experiment_name)

    for systems in systems_sets:
        sets_of_hits = [
            SetOfHits.from_XML(get_output_path(system)) for system in systems
        ]
        combined_set_of_hits = combine_sets_of_hits(sets_of_hits)

        output_file_name = "_+_".join(systems)
        output_file_path = (
            OUTPUT_PATH / "system-combination" / f"{output_file_name}.xml"
        )
        combined_set_of_hits.write_hits_to_file(output_file_path)

        mtwvs = get_MTWVs_for_output_file(output_file_path)
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


def get_output_path(file_name):
    return OUTPUT_PATH / f"{file_name}.xml"


if __name__ == "__main__":
    main()