#!/usr/bin/python3

import json
import random
import numpy as np
import langdetect
from string import ascii_lowercase
from collections import defaultdict

class Attack():
    def __init__(self):
        self.freq_english_bigrams = self.__load_english_bigrams()
        self.ciphertext = self.__load_ciphertext()
        self.matrix = np.chararray(shape = (5,5))


    def start(self):
        #1. Populate the matrix with random permutations of the 25 letters
        self.__randomly_populate_matrix()

        #2. Decrypt using the current decryption matrix
        self.__decrypt_attempt()

    def __decrypt_attempt(self):
        pairs_cipher = []
        for i in range(0, len(self.ciphertext), 2):
            pairs_cipher.append(self.ciphertext[i] + self.ciphertext[i+1])

        #DECRYPTION RULES
        #Rule 1: Two ciphertext letters in same row -> letter to the left (circular)
        #Rule 2: Two ciphertext letters in the same column -> letter to the top (circular)
        #Rule 3: Otherwise -> letter[own_row][column_occupied_by_other_ciphertext]

        plaintext= ""
        for letter1, letter2 in pairs_cipher:
            location_letter1 = np.where(self.matrix == letter1.encode())
            location_letter2 = np.where(self.matrix == letter2.encode())

            row1, col1 = location_letter1[0][0], location_letter1[1][0]
            row2, col2 = location_letter2[0][0], location_letter2[1][0]

            if row1 == row2:
                plaintext += self.matrix[row1][(col1-1)%5].decode()
                plaintext += self.matrix[row2][(col2-1)%5].decode()

            elif col1 == col2:
                plaintext += self.matrix[(row1-1)%5][col1].decode()
                plaintext += self.matrix[(row2-1)%5][col2].decode()

            else:
                plaintext += self.matrix[row1][col2].decode()
                plaintext += self.matrix[row2][col1].decode()

        return plaintext


    def __randomly_populate_matrix(self):
        alphabet = list(ascii_lowercase)
        alphabet.remove("j")
        random.shuffle(alphabet)

        row, col = 0, 0
        for index, letter in enumerate(alphabet):
            self.matrix[row][col] = letter
            col += 1
            if (index+1) % 5 == 0:
                row += 1
                col = 0


    def __load_english_bigrams(self):
        with open("data/freq_english_bigrams.json") as f:
            bigrams_json = json.load(f)

        freq_english_bigrams = defaultdict(lambda: 0)
        for bigram, freq in bigrams_json:
            freq /= 10**8 #scale down
            freq_english_bigrams[bigram] = freq

        return freq_english_bigrams


    def __load_ciphertext(self):
        with open("data/ciphertext.txt", "r") as f:
            ciphertext = f.read()

        return ciphertext.strip().lower()

Attack().start()
