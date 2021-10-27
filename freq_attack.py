#!/usr/bin/python3

import json
import random
import numpy as np
import langdetect
from string import ascii_lowercase
from collections import defaultdict, Counter

class Attack():
    def __init__(self):
        self.freq_english_bigrams = self.__load_english_bigrams()
        self.ciphertext = self.__load_ciphertext()
        self.matrix = np.chararray(shape = (5,5))


    def start(self):
        #1. Populate the matrix with random permutations of the 25 letters
        self.__randomly_populate_matrix()

        min_error = 1000
        iteration = 0
        num_iteration_no_improvement = 0
        best_matrix = self.matrix.copy()
        while True:
            iteration += 1

            if num_iteration_no_improvement == 1000:
                self.matrix = best_matrix.copy()
                print("Copied back best matrix.")

            #2. Decrypt using the current decryption matrix
            plaintext = self.__decrypt_attempt()

            #3. Score the decryption based upon how well the decrypted cipherext matches expected frequencies
            freq_plaintext = self.__calculate_freq_plaintext(plaintext)
            error = self.__score_decrypt_attempt(freq_plaintext)

            if error < min_error:
                print(plaintext)
                print(f"Iteracija: {iteration} -> {error}")
                best_matrix = self.matrix.copy()
                num_iteration_no_improvement = 0
            else:
                num_iteration_no_improvement += 1

            min_error = min(min_error, error)

            #4. Transform the matrix using one of the following operations:
            #   reflection, rotation of a row, rotation of a column, switching two letters
            self.__transform_matrix()


    def __transform_matrix(self):
        method = random.randint(1,9)

        #1. Mirror on x axis
        if method == 1:
            self.matrix = np.flip(self.matrix, axis=0)

        #2. Mirror on y axis
        elif method == 2:
            self.matrix = np.flip(self.matrix, axis=1)

        #3. Swap 2 elements
        elif method == 3:
            row1, row2 = random.sample(range(0,5), 2)
            col1, col2 = random.sample(range(0,5), 2)
            self.matrix[row1, col1], self.matrix[row2, col2] = self.matrix[row2, col2], self.matrix[row1, col1]

        #4. Swap 2 rows
        elif method == 4:
            row1, row2 = random.sample(range(0,5), 2)
            self.matrix[ [row1, row2] ] = self.matrix[ [row2, row1] ]

        #5. Swap 2 columns
        elif method == 5:
            col1, col2 = random.sample(range(0,5), 2)
            self.matrix[:, col1], self.matrix[:, col2] = self.matrix[:, col2], self.matrix[:, col1].copy()

        #6. Permute 5 rows
        elif method == 6:
            np.random.shuffle(self.matrix)

        #7. Permute 5 columns
        elif method == 7:
            col_order = [0, 1, 2, 3, 4]
            random.shuffle(col_order)
            self.matrix = self.matrix[:, col_order]

        #8. Permute elements of any row
        elif method == 8:
            row = random.randint(0,4)
            np.random.shuffle(self.matrix[row])

        #9. Permute elements of any column
        elif method == 9:
            col = random.randint(0, 4)
            np.random.shuffle(self.matrix[:,col])


    def __score_decrypt_attempt(self, freq_plaintext):
        error = 0
        for pair, attempt_freq in freq_plaintext.items():
            real_freq = self.freq_english_bigrams[pair]
            error += abs(real_freq - attempt_freq)

        return error


    def __calculate_freq_plaintext(self, plaintext):
        pairs_plain = []
        for i in range(0, len(self.ciphertext), 2):
            pairs_plain.append(plaintext[i] + plaintext[i+1])

        counter = Counter(pairs_plain)
        total_freq = sum(counter.values())

        freq_plaintext = defaultdict(lambda: 0.0)
        for pair in counter:
            freq_plaintext[pair] = counter[pair] / total_freq

        return freq_plaintext


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

        freq_english_bigrams = defaultdict(lambda: 0.0)

        total_freq = 0
        for bigram, freq in bigrams_json:
            total_freq += freq

        for bigram, freq in bigrams_json:
            freq_english_bigrams[bigram] = freq / total_freq

        return freq_english_bigrams


    def __load_ciphertext(self):
        with open("data/ciphertext.txt", "r") as f:
            ciphertext = f.read()

        return ciphertext.strip().lower()

Attack().start()
