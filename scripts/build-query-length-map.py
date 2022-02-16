from collections import defaultdict
from queries import Queries
from constants.paths import QUERIES_PATH
from util.file_writer import write_to_file

queries_file_name = "queries-word.xml"
queries = Queries.from_queries_file(QUERIES_PATH / queries_file_name).queries_dict

query_length_map = {kwid: len(kwtext.split()) for kwid, kwtext in queries.items()}

query_length_map_text = ""
query_length_counters = defaultdict(int)
for i, kwid in enumerate(queries.keys(), start=1):
    query_length = query_length_map[kwid]
    query_length_counters[query_length] += 1
    query_length_count = query_length_counters[query_length]
    query_length_map_text += f"{query_length} {i:05} {query_length_count:05}\n"

write_to_file(query_length_map_text, QUERIES_PATH / "query-length.map")
