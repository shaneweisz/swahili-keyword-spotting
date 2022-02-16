import argparse
from constants.paths import CTMS_PATH, OUTPUT_PATH, QUERIES_PATH
from index import Index
from set_of_hits import SetOfHits
from queries import Queries


def run_kws(ctm_file_path, queries_file_path, output_file_path, use_oov_proxies):
    index = Index.from_ctm(ctm_file_path)
    queries = Queries.from_queries_file(queries_file_path)
    set_of_hits = SetOfHits.from_search(queries, index, use_oov_proxies)
    set_of_hits.write_hits_to_file(output_file_path)


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
    arg_parser.add_argument(
        "--use_oov_proxies",
        type=bool,
        help="Whether to use proxy keywords",
        required=False,
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    ctm_file_path = CTMS_PATH / args.ctm
    queries_file_path = QUERIES_PATH / args.queries
    output_file_path = OUTPUT_PATH / args.output
    use_oov_proxies = args.use_oov_proxies

    run_kws(ctm_file_path, queries_file_path, output_file_path, use_oov_proxies)
