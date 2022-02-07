from typing import Dict, List
import os
from index import Hit

HITS_FILE_HEADER = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n'  # noqa
HITS_FILE_FOOTER = "</kwslist>"
HIT_HEADER = '<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">\n'
HIT_FOOTER = "</detected_kwlist>\n"


class KWS_Hits:
    def __init__(self, kwid_to_hits: Dict[str, Hit]):
        self.kwid_to_hits = kwid_to_hits

    @classmethod
    def from_XML(output_filename: str):
        """Takes in an `output/<name>.xml` file and builds a KWS_Hits object."""
        pass

    def write_hits_to_file(self, output_filename: str):
        formatted_hits = self._format_hits_for_output()
        KWS_Hits.write_to_file(formatted_hits, output_filename)

    def _format_hits_for_output(self):
        output = HITS_FILE_HEADER
        for kwid, hits in self.kwid_to_hits.items():
            output += KWS_Hits._output_for_hit(kwid, hits)
        output += HITS_FILE_FOOTER
        return output

    @staticmethod
    def _output_for_hit(kwid: str, hits: List[Hit]):
        output = HIT_HEADER.format(kwid=kwid)
        for hit in hits:
            output += f'<kw file="{hit.kw_file}" '
            output += f'channel="{hit.channel}" '
            output += f'tbeg="{hit.start_time}" '
            output += f'dur="{hit.duration}" '
            output += f'score="{hit.score}" '
            output += 'decision="YES"/>\n'
        output += HIT_FOOTER
        return output

    @staticmethod
    def write_to_file(content: str, filename: str):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(content)
