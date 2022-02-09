from constants.paths import OUTPUT_PATH
from helpers.score_system import get_MTWV_for_output_file

experiment_name = "01-kws"

output_file_names_to_score = [
    "reference.xml",
    "onebest-word.xml",
    "onebest-morph.xml",
    "onebest-word-to-morph.xml",
]

results_file = open(f"{experiment_name}.csv", "w")

for output_file_name in output_file_names_to_score:
    output_file_path = OUTPUT_PATH / output_file_name
    mtwv = get_MTWV_for_output_file(output_file_path)
    print(output_file_name, mtwv)
    results_file.write(f"{output_file_name},{mtwv}\n")
    results_file.flush()

results_file.close()
