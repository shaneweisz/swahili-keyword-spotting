from __future__ import annotations
from itertools import chain


class Hit:
    def __init__(self, file, channel, tbeg, dur, score):
        self.file = file
        self.channel = int(channel)
        self.tbeg = float(tbeg)
        self.dur = float(dur)
        self.score = float(score)

    def update_score(self, new_score: float):
        self.score = new_score

    def in_same_file(self, other_hit: Hit):
        return self.file == other_hit.file

    def overlaps_with(self, other_hit: Hit):
        start1, start2 = self.tbeg, other_hit.tbeg
        end1, end2 = start1 + self.dur, start2 + other_hit.dur
        return (start1 <= end2) and (start2 <= end1)

    def __str__(self):
        return f'<kw file="{self.file}" channel="{self.channel}" tbeg="{self.tbeg}" dur="{self.dur}" score="{self.score}" decision="YES"/>\n'  # noqa


class HitList:
    def __init__(self, hit_list=[]):
        self.hit_list = hit_list.copy()

    def add_hit(self, hit: Hit):
        self.hit_list.append(hit)

    def normalize_scores(self, gamma):
        sum_of_scores = sum([hit.score**gamma for hit in self.hit_list])
        for i, hit in enumerate(self.hit_list):
            normalised_score = (hit.score**gamma) / sum_of_scores
            self.hit_list[i].update_score(normalised_score)

    def combine_with(self, other_hit_list: HitList) -> HitList:
        new_hit_list = self.hit_list.copy()
        for hit in self.hit_list:
            for other_hit in other_hit_list.hit_list:
                if hit.in_same_file(other_hit) and hit.overlaps_with(other_hit):
                    file = hit.file
                    channel = hit.channel
                    tbeg = hit.tbeg if hit.score > other_hit.score else other_hit.tbeg
                    dur = hit.dur if hit.score > other_hit.score else other_hit.dur
                    score = (hit.score + other_hit.score) / 2
                    new_hit = Hit(file, channel, tbeg, dur, score)
                    new_hit_list.append(new_hit)
        return HitList(new_hit_list)

    def __str__(self):
        return "".join([str(hit) for hit in self.hit_list])
