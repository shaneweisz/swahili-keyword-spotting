from scorer import get_TWV_for_ctm_file

ctm_filenames = ["reference.ctm", "decode.ctm"]

for ctm_filename in ctm_filenames:
    output_filename = ctm_filename.replace(".ctm", ".xml")
    print(ctm_filename, get_TWV_for_ctm_file(ctm_filename, output_filename))
