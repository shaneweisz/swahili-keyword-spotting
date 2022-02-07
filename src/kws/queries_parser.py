from typing import Dict
from bs4 import BeautifulSoup


def parse_queries_file(queries_file_path: str) -> Dict[str, str]:
    queries = {}

    with open(queries_file_path) as queries_file:
        xml_str = queries_file.read()
        soup = BeautifulSoup(xml_str, features="xml")

    kws = soup.find_all("kw")
    for kw in kws:
        kwid = kw.get("kwid")
        kwtext = kw.kwtext.text.lower()
        queries[kwid] = kwtext

    return queries
