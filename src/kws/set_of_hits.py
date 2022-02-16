# The `from __future__ import annotations` allows `combine_hits` to take in a typed `KWS_Hits` object. See: # noqa
# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations
from collections import defaultdict
from typing import Dict

from bs4 import BeautifulSoup
from index import Index
from queries import Queries
from util.file_writer import write_to_file
from hits import Hit, HitList
from oov_to_iv import GraphemeConfusions


HITS_FILE_HEADER = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n'  # noqa
HITS_FILE_FOOTER = "</kwslist>"
HIT_HEADER = '<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">\n'
HIT_FOOTER = "</detected_kwlist>\n"


class SetOfHits:
    def __init__(self, kwid_to_hits: Dict[str, HitList]):
        self.kwid_to_hits: Dict[str, HitList] = kwid_to_hits

    @classmethod
    def from_search(cls, queries: Queries, index: Index, use_oov_proxies: bool):
        kwid_to_hits = dict()
        for kwid, kwtext in queries.queries_dict.items():
            search_text = kwtext
            if use_oov_proxies and queries.is_oov(kwid):
                query_words = kwtext.split(" ")
                gc = GraphemeConfusions()
                iv_words = [gc.closest_iv_word(word)[0] for word in query_words]
                search_text = " ".join(iv_words)
            kwid_to_hits[kwid] = index.search(search_text)
        set_of_hits = cls(kwid_to_hits)
        return set_of_hits

    @classmethod
    def from_XML(cls, xml_file_path: str):
        kwid_to_hits = defaultdict(HitList)

        with open(xml_file_path) as xml_file:
            xml_str = xml_file.read()
            soup = BeautifulSoup(xml_str, features="xml")

        kw_lists = soup.find_all("detected_kwlist")
        for kw_list in kw_lists:
            kwid = kw_list.get("kwid")
            for kw in kw_list.find_all("kw"):
                hit = Hit(
                    kw["file"],
                    kw["channel"],
                    tbeg=kw["tbeg"],
                    dur=kw["dur"],
                    score=kw["score"],
                )
                kwid_to_hits[kwid].add_hit(hit)

        set_of_hits = cls(kwid_to_hits)
        return set_of_hits

    def write_hits_to_file(self, output_file_path: str):
        formatted_hits = self._format_for_output()
        write_to_file(formatted_hits, output_file_path)

    def normalise_scores(self, gamma: int):
        for hit_list in self.kwid_to_hits.values():
            hit_list.normalize_scores(gamma)

    def _format_for_output(self):
        output = HITS_FILE_HEADER
        for kwid, hit_list in self.kwid_to_hits.items():
            output += SetOfHits._output_for_kwid(kwid, hit_list)
        output += HITS_FILE_FOOTER
        return output

    @staticmethod
    def _output_for_kwid(kwid: str, hit_list: HitList):
        output = HIT_HEADER.format(kwid=kwid)
        output += str(hit_list)
        output += HIT_FOOTER
        return output
