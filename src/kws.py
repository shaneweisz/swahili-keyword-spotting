from typing import Dict, List
from index import Index, Hit
from output import KWS_Hits
from parse_queries import parse_queries_file


def run_kws(ctm_filename, queries_filename, output_filename):
    index = Index.from_ctm_file(ctm_filename)
    queries = parse_queries_file(queries_filename)
    kwid_to_hits = generate_all_hits(queries, index)
    KWS_Hits(kwid_to_hits).write_hits_to_file(output_filename)


def generate_all_hits(queries: Dict[str, str], index: Index) -> Dict[str, List[Hit]]:
    kwid_to_hits = dict()
    for kwid, kwtext in queries.items():
        kwid_to_hits[kwid] = index.search_for_all_hits(kwtext)
    return kwid_to_hits


def normalize_scores(hits):
    pass
