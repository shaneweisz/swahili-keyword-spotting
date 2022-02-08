class Hit:
    def __init__(self, kw_file, channel, tbeg, dur, score):
        self.kw_file = kw_file
        self.channel = int(channel)
        self.tbeg = float(tbeg)
        self.dur = float(dur)
        self.score = float(score)

    def update_score(self, new_score: float):
        self.score = new_score

    def __str__(self):
        return f'<kw file="{self.kw_file}" channel="{self.channel}" tbeg="{self.tbeg}" dur="{self.dur}" score="{self.score}" decision="YES"/>\n'  # noqa


class HitList:
    def __init__(self, hit_list=[]):
        self.hit_list = hit_list.copy()

    def add_hit(self, hit: Hit):
        self.hit_list.append(hit)

    def __str__(self):
        return "".join([str(hit) for hit in self.hit_list])
