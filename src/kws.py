from index import Index
from set_of_hits import SetOfHits
from queries_parser import parse_queries_file


def run_kws(ctm_filename, queries_filename, output_filename):
    index = Index.from_ctm_file(ctm_filename)
    queries = parse_queries_file(queries_filename)
    set_of_hits = SetOfHits.search(queries, index)
    set_of_hits.write_hits_to_file(output_filename)
