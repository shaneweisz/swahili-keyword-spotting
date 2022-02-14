from __future__ import annotations
from collections import defaultdict, namedtuple
from itertools import chain
from typing import List
import numpy as np


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


class SystemHit(Hit):
    def __init__(self, system_index, hit):
        super().__init__(hit.file, hit.channel, hit.tbeg, hit.dur, hit.score)
        self.system_index = system_index


class HitList:
    def __init__(self, hit_list=[]):
        self.hit_list: List[Hit] = hit_list.copy()

    def add_hit(self, hit: Hit):
        self.hit_list.append(hit)

    def normalize_scores(self, gamma):
        sum_of_scores = sum([hit.score**gamma for hit in self.hit_list])
        for i, hit in enumerate(self.hit_list):
            normalised_score = (hit.score**gamma) / sum_of_scores
            self.hit_list[i].update_score(normalised_score)

    def combine_with(
        self, other_hit_lists: List[HitList], weightings: List[float] | None = None
    ) -> HitList:
        # hit_lists_per_file = []  # contains a list of `file_to_hit_list` dicts
        # for hit_list in hit_lists:
        #     file_to_hit_list = defaultdict(list)
        #     for hit in hit_list.hit_list:
        #         file = hit.file
        #         file_to_hit_list[file].append(hit)
        #     hit_lists_per_file.append(file_to_hit_list)

        combined_hit_list = [SystemHit(0, hit) for hit in self.hit_list]
        for i, hit_list in enumerate(other_hit_lists, start=1):
            combined_hit_list += [SystemHit(i, hit) for hit in hit_list.hit_list]

        combined_hit_list = sorted(
            combined_hit_list, key=lambda hit: (hit.file, hit.tbeg)
        )
        # combined_hit_list = sorted(combined_hit_list, key=lambda hit: hit.file)

        new_hit_list = []
        i = 0
        while i < len(combined_hit_list):
            current_hit = combined_hit_list[i]
            hits_to_merge = [current_hit]

            j = 1
            while i + j < len(combined_hit_list):
                next_hit = combined_hit_list[i + j]
                if not current_hit.in_same_file(
                    next_hit
                ) or not current_hit.overlaps_with(next_hit):
                    break
                hits_to_merge.append(next_hit)
                j += 1

            if len(hits_to_merge) == 1:
                new_hit_list.append(current_hit)
            else:
                file = current_hit.file
                channel = current_hit.channel
                max_score_index = 0
                max_score = -1
                for index, hit in enumerate(hits_to_merge):
                    if hit.score > max_score:
                        max_score = hit.score
                        max_score_index = index
                tbeg = hits_to_merge[max_score_index].tbeg
                dur = hits_to_merge[max_score_index].dur
                score = sum([hit.score for hit in hits_to_merge])
                new_hit = Hit(file, channel, tbeg, dur, score)
                new_hit_list.append(new_hit)

            i += len(hits_to_merge)

        return HitList(new_hit_list)

    def __str__(self):
        return "".join([str(hit) for hit in self.hit_list])
