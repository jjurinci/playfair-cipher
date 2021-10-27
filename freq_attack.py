#!/usr/bin/python3

import json
from collections import defaultdict

class Attack():
    def __init__(self):
        self.freq_english_bigrams = self.load_english_bigrams()
        self.ciphertext = self.load_ciphertext()

    def load_english_bigrams(self):
        with open("data/freq_english_bigrams.json") as f:
            bigrams_json = json.load(f)

        freq_english_bigrams = defaultdict(lambda: 0)
        for bigram, freq in bigrams_json:
            freq /= 10**8 #scale down
            freq_english_bigrams[bigram] = freq

        return freq_english_bigrams

    def load_ciphertext(self):
        with open("data/ciphertext.txt", "r") as f:
            ciphertext = f.read()

        return ciphertext.strip()

