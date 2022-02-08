from set_of_hits import SetOfHits
from constants.paths import OUTPUT_PATH


def do_sto_normalisation(gamma_STO, input_xml_file_path, output_xml_file_path):
    set_of_hits = SetOfHits.from_XML(input_xml_file_path)
    set_of_hits.normalise_scores(gamma_STO)
    set_of_hits.write_hits_to_file(output_xml_file_path)


if __name__ == "__main__":
    gamma_STO = 5
    input_xml_file_path = OUTPUT_PATH / "decode.xml"
    output_xml_file_path = OUTPUT_PATH / f"decode-STO{gamma_STO}.xml"
    do_sto_normalisation(gamma_STO, input_xml_file_path, output_xml_file_path)
