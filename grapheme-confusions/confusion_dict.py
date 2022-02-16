from collections import defaultdict
from constants.paths import LIB_PATH

grapheme_map_file_path = LIB_PATH / "kws" / "grapheme.map"


def get_confusion_dict():
    confusion_dict = defaultdict(lambda: defaultdict(int))
    with open(grapheme_map_file_path) as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip("\n")
        c1, c2, num_times = line.split()
        confusion_dict[c1][c2] = int(num_times)
    return confusion_dict


def normalise_confusion_dict(confusion_dict):
    for c1 in confusion_dict:
        tot = sum(confusion_dict[c1].values())
        for c2 in confusion_dict[c1]:
            confusion_dict[c1][c2] = confusion_dict[c1][c2] / tot
    return confusion_dict


d = get_confusion_dict()
d = normalise_confusion_dict(d)
print(d)
