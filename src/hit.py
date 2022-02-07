class Hit:
    def __init__(self, kw_file, channel, start_time, duration, score):
        self.kw_file = kw_file
        self.channel = int(channel)
        self.start_time = float(start_time)
        self.duration = float(duration)
        self.score = float(score)

    def update_score(self, new_score: float):
        self.score = new_score
