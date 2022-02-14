from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file
from set_of_hits import SetOfHits

experiment_name = "onebest-kws"

output_file_names_to_score = [
    "reference.xml",
    "onebest-word.xml",
    "onebest-morph.xml",
    "onebest-word-to-morph.xml",
]

RESULTS_HEADER = "file,all,iv,oov"


def main():
    results_file = setup_results_file(experiment_name)

    for output_file_name in output_file_names_to_score:
        mtwvs = get_MTWVs_for_output_file(OUTPUT_PATH / output_file_name)
        line = get_results_line(mtwvs, output_file_name)
        write_line_to_file(results_file, line)

        normalised_output_file_name = normalise(output_file_name, gamma=1)
        mtwvs = get_MTWVs_for_output_file(OUTPUT_PATH / normalised_output_file_name)
        line = get_results_line(mtwvs, normalised_output_file_name)
        write_line_to_file(results_file, line)

    cleanup_results_file(results_file)


def normalise(output_file_name, gamma):
    set_of_hits = SetOfHits.from_XML(OUTPUT_PATH / output_file_name)
    set_of_hits.normalise_scores(gamma)

    normalised_output_file_name = get_normalised_file_name(output_file_name, gamma)
    normalised_output_file_path = OUTPUT_PATH / normalised_output_file_name
    set_of_hits.write_hits_to_file(normalised_output_file_path)

    return normalised_output_file_name


def get_normalised_file_name(output_file_name, gamma):
    return output_file_name.strip(".xml") + "-STO.xml"


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
