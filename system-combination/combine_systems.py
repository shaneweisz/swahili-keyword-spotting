from typing import List
from hits import Hit, HitList, SystemHit
from set_of_hits import SetOfHits


def combine_sets_of_hits(
    sets_of_hits: List[SetOfHits],
    method="CombSum",
    weights: List[float] = None,
) -> SetOfHits:
    new_kwid_to_hits = dict()
    kwids = [f"KW202-00{i:03}" for i in range(1, 501)]
    for kwid in kwids:
        hit_lists = [set_of_hits.kwid_to_hits[kwid] for set_of_hits in sets_of_hits]
        combined_hit_list = combine_hit_lists(hit_lists, method, weights)
        new_kwid_to_hits[kwid] = combined_hit_list
    return SetOfHits(new_kwid_to_hits)


def combine_hit_lists(
    hit_lists: HitList,
    method,
    weights: List[float],
) -> HitList:
    combined_hit_list = []
    for i, hit_list in enumerate(hit_lists):
        combined_hit_list += [SystemHit(i, hit) for hit in hit_list.hit_list]

    combined_hit_list = sorted(combined_hit_list, key=lambda hit: (hit.file, hit.tbeg))

    new_hit_list = []
    i = 0
    while i < len(combined_hit_list):
        current_hit = combined_hit_list[i]
        hits_to_merge = [current_hit]

        j = 1
        while i + j < len(combined_hit_list):
            next_hit = combined_hit_list[i + j]
            if not (
                current_hit.in_same_file(next_hit)
                and current_hit.overlaps_with(next_hit)
            ):
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
            if method == "CombSUM":
                score = sum([hit.score for hit in hits_to_merge])
            elif method == "CombMNZ":
                score = len(hits_to_merge) * sum([hit.score for hit in hits_to_merge])
            elif method == "WCombMNZ":
                weights_total = sum(weights)
                score = len(hits_to_merge) * sum(
                    [
                        hit.score * (weights[hit.system_index] / weights_total)
                        for hit in hits_to_merge
                    ]
                )
            else:
                raise Exception("Invalid Score Merging Method")
            new_hit = Hit(file, channel, tbeg, dur, score)
            new_hit_list.append(new_hit)
        i += len(hits_to_merge)

    return HitList(new_hit_list)
