from typing import Dict
from bs4 import BeautifulSoup
from constants.paths import QUERIES_PATH


class Queries:
    def __init__(self, queries_dict: Dict[str, str]):
        self.queries_dict: Dict[str, str] = queries_dict
        self.kwid_to_oov = self.build_kwid_to_oov_dict()

    @classmethod
    def from_queries_file(cls, queries_file_path):
        queries_dict = {}

        with open(queries_file_path) as queries_file:
            xml_str = queries_file.read()
            soup = BeautifulSoup(xml_str, features="xml")

        kws = soup.find_all("kw")
        for kw in kws:
            kwid = kw.get("kwid")
            kwtext = kw.kwtext.text.lower()
            queries_dict[kwid] = kwtext

        queries = cls(queries_dict)
        return queries

    def build_kwid_to_oov_dict(self):
        file_path = QUERIES_PATH / "ivoov.map"
        kwid_to_oov = dict()
        with open(file_path) as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            tokens = line.split()
            iv_oov_tag = tokens[0]
            kwid = "KW202-" + tokens[1]
            kwid_to_oov[kwid] = True if iv_oov_tag == "oov" else False
        return kwid_to_oov

    def is_oov(self, kwid):
        return self.kwid_to_oov[kwid]
