# The `from __future__ import annotations` allows `combine_hits` to take in a typed `KWS_Hits` object. See: # noqa
# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations
from typing import Dict
from index import Index
from util.file_writer import write_to_file
from hits import HitList


HITS_FILE_HEADER = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n'  # noqa
HITS_FILE_FOOTER = "</kwslist>"
HIT_HEADER = '<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">\n'
HIT_FOOTER = "</detected_kwlist>\n"


class SetOfHits:
    def __init__(self, kwid_to_hits: Dict[str, HitList]):
        self.kwid_to_hits = kwid_to_hits

    @classmethod
    def from_search(cls, queries: Dict[str, str], index: Index):
        kwid_to_hits = dict()
        for kwid, kwtext in queries.items():
            kwid_to_hits[kwid] = index.search(kwtext)
        hits = cls(kwid_to_hits)
        return hits

    @classmethod
    def from_XML(output_filename: str):
        """Takes in an `output/<name>.xml` file and builds a KWS_Hits object."""
        pass  # TODO: 3.3 in prac handout

    def write_hits_to_file(self, output_filename: str):
        formatted_hits = self._format_for_output()
        write_to_file(formatted_hits, output_filename)

    def combine_with(self, other_set_of_hits: SetOfHits):
        pass  # TODO: 3.3 in prac handout

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
