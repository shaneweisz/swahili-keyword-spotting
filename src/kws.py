from typing import Dict, List
from index import Index, SearchHit
from output import format_hits_output, write_to_file
from parse_queries import parse_queries_file


def run_kws(ctm_filename, queries_filename, output_filename):
    index = Index.from_ctm_file(ctm_filename)
    queries = parse_queries_file(queries_filename)
    kwid_to_hits = generate_all_hits(queries, index)
    formatted_hits = format_hits_output(kwid_to_hits)
    write_to_file(formatted_hits, output_filename)


def generate_all_hits(
    queries: Dict[str, str], index: Index
) -> Dict[str, List[SearchHit]]:
    kwid_to_hits = dict()
    for kwid, kwtext in queries.items():
        kwid_to_hits[kwid] = index.search_for_all_hits(kwtext)
    return kwid_to_hits


def normalize_scores(hits):
    pass
