from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file
from set_of_hits import SetOfHits

experiment_name = "03-combine-onebest"

systems_pairs = [
    ["onebest-word.xml", "onebest-morph.xml"]
    # "onebest-word-to-morph.xml",
]

RESULTS_HEADER = "file,all,iv,oov"


def main():
    results_file = setup_results_file(experiment_name)

    for system_pair in systems_pairs:
        set_of_hits1 = SetOfHits.from_XML(OUTPUT_PATH / system_pair[0])
        # set_of_hits1.normalise_scores(gamma=1)
        set_of_hits2 = SetOfHits.from_XML(OUTPUT_PATH / system_pair[1])
        # set_of_hits2.normalise_scores(gamma=1)
        combined_set_of_hits = set_of_hits1.combine_with(set_of_hits2)
        # combined_set_of_hits.normalise_scores(gamma=1)

        output_file_name = "+".join(system_pair)
        output_file_path = OUTPUT_PATH / "system-combination" / output_file_name
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


if __name__ == "__main__":
    main()
