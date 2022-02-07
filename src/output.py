from typing import Dict, List
import os
from index import SearchHit


HITS_FILE_HEADER = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">'
HITS_FILE_FOOTER = "</kwslist>"
HIT_HEADER = '<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">'
HIT_FOOTER = "</detected_kwlist>"


def format_hits_output(kwid_to_hits: Dict[str, SearchHit]):
    output = HITS_FILE_HEADER + "\n"
    for kwid, hits in kwid_to_hits.items():
        output += output_for_hit(kwid, hits)
    output += HITS_FILE_FOOTER
    return output


def output_for_hit(kwid: str, hits: List[SearchHit]):
    output = HIT_HEADER.format(kwid=kwid) + "\n"
    for hit in hits:
        output += f'<kw file="{hit.kw_file}" '
        output += f'channel="{hit.channel}" '
        output += f'tbeg="{hit.start_time}" '
        output += f'dur="{hit.duration}" '
        output += f'score="{hit.score}" '
        output += 'decision="YES"/>\n'
    output += HIT_FOOTER + "\n"
    return output


def write_to_file(content: str, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(content)
