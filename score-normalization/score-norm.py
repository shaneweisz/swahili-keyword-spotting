import argparse
from constants.paths import OUTPUT_PATH
from set_of_hits import SetOfHits


def normalize_to_new_output_file(xml_output_file_path):
    set_of_hits = SetOfHits.from_XML(xml_output_file_path)
    set_of_hits.normalise_scores(gamma=1)
    new_file_path = xml_output_file_path.parent / ("STO-" + xml_output_file_path.name)
    set_of_hits.write_hits_to_file(new_file_path)


def get_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--xml",
        type=str,
        help="The name of the XML output file to normalize",
        required=True,
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    xml_output_file_path = OUTPUT_PATH / args.xml

    normalize_to_new_output_file(xml_output_file_path)
