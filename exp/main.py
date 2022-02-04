import argparse
from index import Index


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--ctm", type=str, help="The path to the input CTM file", required=True
    )

    args = arg_parser.parse_args()
    ctm_file = args.ctm

    index = Index.from_ctm_file(ctm_file)

    print(index.get_index().keys())


if __name__ == "__main__":
    main()
