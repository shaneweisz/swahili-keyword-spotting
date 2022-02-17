from confusion_dict import get_confusion_dict, normalise_confusion_dict
from iv_words import get_iv_words


class GraphemeConfusions:
    def __init__(self):
        self.confusion_dict = get_confusion_dict()
        self.confusion_dict = normalise_confusion_dict(self.confusion_dict)
        self.iv_words = get_iv_words()

    def is_iv_word(self, word):
        return word in self.iv_words

    def closest_iv_word(self, oov_word):
        min_dist = 1000000000
        min_dist_iv_word = None
        for iv_word in self.iv_words:
            dist = self.weighted_lev_distance(oov_word, iv_word)
            if dist < min_dist:
                min_dist = dist
                min_dist_iv_word = iv_word
        return min_dist_iv_word

    def weighted_lev_distance(self, s0, s1):
        if s0 == s1:
            return 0.0

        v0, v1 = [0.0] * (len(s1) + 1), [0.0] * (len(s1) + 1)

        v0[0] = 0
        for i in range(1, len(v0)):
            v0[i] = v0[i - 1] + self.insertion_cost_fn(s1[i - 1])

        for i in range(len(s0)):
            s0i = s0[i]
            deletion_cost = self.deletion_cost_fn(s0i)
            v1[0] = v0[0] + deletion_cost

            for j in range(len(s1)):
                s1j = s1[j]
                cost = 0
                if s0i != s1j:
                    cost = self.substitution_cost_fn(s0i, s1j)
                insertion_cost = self.insertion_cost_fn(s1j)
                v1[j + 1] = min(
                    v1[j] + insertion_cost, v0[j + 1] + deletion_cost, v0[j] + cost
                )
            v0, v1 = v1, v0

        return v0[len(s1)]

    def similarity_prob(self, s0, s1):
        m_len = max(len(s0), len(s1))
        if m_len == 0:
            return 0.0
        return 1.0 - self.weighted_lev_distance(s0, s1) / m_len

    def insertion_cost_fn(self, char):
        return 1 - self.confusion_dict["sil"][char]

    def deletion_cost_fn(self, char):
        return 1 - self.confusion_dict[char]["sil"]

    def substitution_cost_fn(self, char_a, char_b):
        return 1 - self.confusion_dict[char_a][char_b]
