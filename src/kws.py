# This contains a KWS class that takes in a CTM file, builds an indexer,
# takes in a queries file, generates hits for each query, and writes it to a file
from typing import Dict, List
from index import Index
from index import SearchHit
import os


class KWS:
    def run_kws(self, ctm_filename, queries_filename, output_filename):
        index = Index.from_ctm_file(ctm_filename)
        queries = self.parse_queries_file(queries_filename)
        kwid_to_hits = self.generate_all_hits(queries, index)
        formatted_hits = self.format_hits_output(kwid_to_hits)
        self.write_to_file(formatted_hits, output_filename)

    def parse_queries_file(self, queries_filename: str):
        kwids = []
        kwtexts = []
        with open(queries_filename) as queries_file:
            for line in queries_file.readlines():
                line = line.strip("\n")
                if "kwid" in line:
                    kwid = line[line.find('"') + 1 : -1 * len('">')]
                    kwids.append(kwid)
                elif "kwtext" in line:
                    kwtext = line[line.find(">") + 1 : -1 * len("</kwtext>")]
                    kwtexts.append(kwtext)
        queries = {kwid: kwtext for kwid, kwtext in zip(kwids, kwtexts)}
        return queries

    def generate_all_hits(
        self, queries: Dict[str, str], index: Index
    ) -> Dict[str, List[SearchHit]]:
        kwid_to_hits = dict()
        for kwid, kwtext in queries.items():
            kwid_to_hits[kwid] = index.search_for_all_hits(kwtext)
        return kwid_to_hits

    def normalize_scores(self, hits):
        pass

    def output_for_hit(self, kwid: str, hits: List[SearchHit]):
        header = f'<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">'
        footer = "</detected_kwlist>"

        output = header + "\n"
        for hit in hits:
            output += f'<kw file="{hit.kw_file}" '
            output += f'channel="{hit.channel}" '
            output += f'tbeg="{hit.start_time}" '
            output += f'dur="{hit.duration}" '
            output += f'score="{hit.score}" '
            output += 'decision="YES"/>\n'
        output += footer + "\n"

        return output

    def format_hits_output(self, kwid_to_hits):
        header = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" '
        header += 'language="swahili" system_id="">'
        footer = "</kwslist>"

        output = header + "\n"
        for kwid, hits in kwid_to_hits.items():
            output += self.output_for_hit(kwid, hits)
        output += footer

        return output

    def write_to_file(self, content: str, filename: str):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(content)
