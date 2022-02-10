from constants.paths import OUTPUT_PATH, RESULTS_PATH
from helpers.score_system import get_MTWVs_for_output_file
from kws.set_of_hits import SetOfHits

experiment_name = "01-onebest_kws"

output_file_names_to_score = [
    "reference.xml",
    "onebest-word.xml",
    "onebest-morph.xml",
    "onebest-word-to-morph.xml",
]


def main():

    results_file = open(RESULTS_PATH / f"{experiment_name}.csv", "w")

    for output_file_name in output_file_names_to_score:
        output_file_path = OUTPUT_PATH / output_file_name
        mtwvs = get_MTWVs_for_output_file(output_file_path)
        line = f"{output_file_name},{mtwvs.all:.3f},{mtwvs.iv:.3f},{mtwvs.oov:.3f}"
        print(line)
        results_file.write(line + "\n")
        results_file.flush()

    for gamma in [1, 2, 3]:
        sto_output_file_names = []
        for output_file_name in output_file_names_to_score:
            output_file_path = OUTPUT_PATH / output_file_name
            set_of_hits = SetOfHits.from_XML(output_file_path)
            set_of_hits.normalise_scores(gamma)

            sto_output_file_name = output_file_name.strip(".xml") + f"-sto{gamma}.xml"
            sto_output_file_path = OUTPUT_PATH / f"STO{gamma}" / sto_output_file_name
            set_of_hits.write_hits_to_file(sto_output_file_path)
            sto_output_file_names.append(sto_output_file_name)

        for sto_output_file_name in sto_output_file_names:
            sto_output_file_path = OUTPUT_PATH / f"STO{gamma}" / sto_output_file_name
            mtwvs = get_MTWVs_for_output_file(sto_output_file_path)
            line = (
                f"{sto_output_file_name},{mtwvs.all:.3f},{mtwvs.iv:.3f},{mtwvs.oov:.3f}"
            )
            print(line)
            results_file.write(line + "\n")
            results_file.flush()

    results_file.close()


if __name__ == "__main__":
    main()
