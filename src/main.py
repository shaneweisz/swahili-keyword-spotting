import argparse
from kws import run_kws
from constants.paths import CTMS_PATH, OUTPUT_PATH, QUERIES_PATH


def main():
    args = get_args()

    ctm_filename = CTMS_PATH / args.ctm
    queries_filename = QUERIES_PATH / args.queries
    output_filename = OUTPUT_PATH / args.output

    run_kws(ctm_filename, queries_filename, output_filename)


def get_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--ctm", type=str, help="The name of the input CTM file", required=True
    )
    arg_parser.add_argument(
        "--queries",
        type=str,
        help="The path to the queries XML file",
        required=True,
    )
    arg_parser.add_argument(
        "--output",
        type=str,
        help="The name of the XML file to write the output to",
        required=True,
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    main()
