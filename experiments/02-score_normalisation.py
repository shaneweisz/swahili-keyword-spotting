from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import MTWVs, get_MTWVs_for_output_file
from kws.set_of_hits import SetOfHits

experiment_name = "02-score_normalisation"

output_file_names_to_score = [
    "reference.xml",
    "onebest-word.xml",
    "onebest-morph.xml",
    "onebest-word-to-morph.xml",
]

RESULTS_HEADER = "file,gamma,all,iv,oov"


def main():
    results_file = setup_results_file(experiment_name)

    for output_file_name in output_file_names_to_score:
        for gamma in [0, 1, 2, 3, 4]:
            normalised_output_file_path = normalise(output_file_name, gamma)
            mtwvs = get_MTWVs_for_output_file(normalised_output_file_path)
            line = get_results_line(mtwvs, output_file_name, gamma)
            write_line_to_file(results_file, line)

    cleanup_results_file(results_file)


def setup_results_file(experiment_name: str):
    results_file_path = RESULTS_PATH / f"{experiment_name}.csv"
    results_file = open(results_file_path, "w")
    write_line_to_file(results_file, RESULTS_HEADER)
    return results_file


def normalise(output_file_name, gamma):
    set_of_hits = SetOfHits.from_XML(OUTPUT_PATH / output_file_name)
    set_of_hits.normalise_scores(gamma)

    normalised_output_file_name = get_normalised_file_name(output_file_name, gamma)
    normalised_output_file_path = (
        OUTPUT_PATH
        / "score-normalisation"
        / f"sto{gamma}"
        / normalised_output_file_name
    )
    set_of_hits.write_hits_to_file(normalised_output_file_path)

    return normalised_output_file_path


def get_results_line(mtwvs: MTWVs, output_file_name: str, gamma: int):
    stripped_output_file_name = output_file_name.strip(".xml")
    line = f"{stripped_output_file_name},{gamma},{mtwvs.all:.3f},{mtwvs.iv:.3f},{mtwvs.oov:.3f}"  # noqa
    return line


def get_normalised_file_name(output_file_name, gamma):
    return output_file_name.strip(".xml") + f"-sto{gamma}.xml"


def write_line_to_file(file, line):
    file.write(line + "\n")
    file.flush()


def cleanup_results_file(file):
    file.close()


if __name__ == "__main__":
    main()
