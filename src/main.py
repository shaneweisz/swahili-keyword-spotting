import argparse
from kws import run_kws


def main():
    args = get_args()
    run_kws(**vars(args))


def get_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--ctm_filename", type=str, help="The path to the input CTM file", required=True
    )
    arg_parser.add_argument(
        "--queries_filename",
        type=str,
        help="The path to the queries XML file",
        required=True,
    )
    arg_parser.add_argument(
        "--output_filename",
        type=str,
        help="The path to which to write the output XML file",
        required=True,
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    main()
