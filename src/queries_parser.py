from typing import Dict


def parse_queries_file(queries_filename: str) -> Dict[str, str]:
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
