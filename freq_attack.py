#!/usr/bin/python3

import random
import math
import numpy as np
from string import ascii_lowercase
from collections import defaultdict

class Attack:
    def __init__(self, file):
        self.quadgrams_freq, self.total_freq_quadgram = self.__load_quadgrams()
        self.ciphertext = self.__load_ciphertext(file)


    """
        Simulated annealing brute force napad na playfair sifru.

        Optimizacijska funkcija provjerava frekvenciju quadgram-ova
        u plaintext-u na nacin da sumira log10 vjerojatnosti quadgram-ova
        u engleskom jeziku.

        Izbjegava lokalne minimume tako da sa vjerojatnoscu od
        e^(difference/temperature) prihvaca "neoptimalnije" rjesenje.
    """
    def brute_force(self, temperature, verbose = True):
        self.parent_key = self.__randomly_populate_key()
        best_key = self.parent_key

        plaintext = self.__decrypt_attempt(self.parent_key)
        best_text = plaintext

        parent_score = self.__calculate_probability(plaintext)
        best_score = parent_score

        for temp in range(temperature, 0, -1):
            for trans in range(50000, 0, -1):
                self.child_key = self.__transform_matrix(self.parent_key[:])

                plaintext = self.__decrypt_attempt(self.child_key)
                child_score = self.__calculate_probability(plaintext)

                dF = child_score - parent_score

                if dF > 0:
                    parent_score = child_score
                    self.parent_key = self.child_key
                else:
                    probability = math.exp(dF / temp)
                    if probability > random.uniform(0,1):
                        parent_score = child_score
                        self.parent_key = self.child_key

                if parent_score > best_score:
                    best_score = parent_score
                    best_key = self.parent_key
                    best_text = plaintext

                    if verbose:
                        print(" \n----------------------------------------")
                        print("\nBest key: ", best_key, "\nBest score: ", best_score,
                                "\nBest plaintext: ", best_text,
                                "\nTemperature: ", temp, " Transition: ", trans)

            if parent_score == best_score:
                break


    """
        Razbija string na substring-ove duljine 4 (quadgram).
        Pr. "ovojeprimjer" -> "ovoj", "voje", "ojep", "jepr", itd...
        Nakon toga, sumira log vjerojatnosti svih quadgram-ova.
    """
    def __calculate_probability(self, deciphered_text):
        sum_of_probability = 0
        for i in range(len(deciphered_text) - 4 + 1):
            quadgram = deciphered_text[i:i+4]
            sum_of_probability += self.__quadgram_log_probability(quadgram)

        return sum_of_probability


    """
        log10 vjerojatnost umjesto normalne vjerojatnosti.
    """
    def __quadgram_log_probability(self, quadgram):
        return math.log10(self.quadgrams_freq[quadgram] / self.total_freq_quadgram)


    """
        Mijenjanje kljuca. Svaka metoda transformacije ima
        odredenu vjerojatnost za svoj poziv.
    """
    def __transform_matrix(self, key: list) -> list:
        choice = random.uniform(0,1)

        #1. Swap 2 elements
        if choice <= 0.9:
            i1, i2 = random.sample(range(0,25), 2)
            key[i1], key[i2] = key[i2], key[i1]

        #2. Reverse a key
        elif choice > 0.9 and choice <= 0.92:
            key.reverse()

        #3. Swap 2 columns
        elif choice > 0.92 and choice <= 0.94:
            col1, col2 = random.sample(range(0,5), 2)
            for i in range(5):
                temp = key[i * 5 + col1]
                key[i * 5 + col1] = key[i * 5 + col2]
                key[i * 5 + col2] = temp

        #4. Swap 2 rows
        elif choice > 0.94 and choice <= 0.96:
            row1, row2 = random.sample(range(0,5), 2)
            for i in range(5):
                temp = key[row1 * 5 + i]
                key[row1 * 5 + i] = key[row2 * 5 + i]
                key[row2 * 5 + i] = temp

        #5. Flip all columns
        elif choice > 0.96 and choice <= 0.98:
            matrix = np.array(key).reshape(5,5)
            for col in range(5):
                for row in range(5//2):
                    temp = matrix[row][col]
                    matrix[row][col] = matrix[5 - row - 1][col]
                    matrix[5 - row - 1][col] = temp

            key = list(np.ravel(matrix))


        #6. Flip all rows
        elif choice > 0.98 and choice <= 1:
            matrix = np.array(key).reshape(5,5)
            for row in range(5):
                for col in range(5//2):
                    temp = matrix[row][col]
                    matrix[row][col] = matrix[row][5 - col - 1]
                    matrix[row][5 - col - 1] = temp

            key = list(np.ravel(matrix))

        return key


    """
        Dekripcija sifrata uz pomoc kljuca.

        DECRYPTION RULES
        Rule 1: Two ciphertext letters in same row -> letter to the left (circular)
        Rule 2: Two ciphertext letters in the same column -> letter to the top (circular)
        Rule 3: Otherwise -> letter[own_row][column_occupied_by_other_ciphertext]
    """
    def __decrypt_attempt(self, key: list):
        plaintext= ""
        for index in range(0, len(self.ciphertext), 2):
            letter1 = self.ciphertext[index]
            letter2 = self.ciphertext[index+1]

            location_letter1 = key.index(letter1)
            location_letter2 = key.index(letter2)

            row1, col1 = location_letter1 // 5, location_letter1 % 5
            row2, col2 = location_letter2 // 5, location_letter2 % 5

            if row1 == row2:
                plaintext += key[row1 * 5 + (col1 + 4) % 5]
                plaintext += key[row2 * 5 + (col2 + 4) % 5]

            elif col1 == col2:
                plaintext += key[(row1 + 4) % 5 * 5 + col1]
                plaintext += key[(row2 + 4) % 5 * 5 + col2]

            else:
                plaintext += key[row1 * 5 + col2]
                plaintext += key[row2 * 5 + col1]

        return plaintext


    """
        Vraca random shufflan-u englesku abecedu bez slova "j".
        Slovo "j" se tipicno izbacuje da bi dobili 25 ukupnih slova.
    """
    def __randomly_populate_key(self) -> list:
        alphabet = list(ascii_lowercase)
        alphabet.remove("j")
        random.shuffle(alphabet)
        return alphabet


    """
        Ucitava listu od 389373 najpopularnijih quadgram-ova u engleskom
        jeziku. Njihova ukupna frekvencija je oko 4224127912.
    """
    def __load_quadgrams(self):
        with open("data/quadgrams.txt", "r") as f:
            quadgrams = f.readlines()

        total_freq_quadgram = 0
        quadgrams_freq = defaultdict(lambda: 1)
        for line in quadgrams:
            quadgram, count = line.split(" ")
            quadgram, count = quadgram.lower(), int(count)
            total_freq_quadgram += count
            quadgrams_freq[quadgram] = count

        return quadgrams_freq, total_freq_quadgram


    """
        Ucitava ciphertext koji je ispravno enkodiran Playfair Cipher
        algoritmom.
    """
    def __load_ciphertext(self, file):
        with open("data/encrypted_text/" + file, "r") as f:
            ciphertext = f.read()
            print("Izracunat broj slova: " + str(len(ciphertext)))

        return ciphertext.strip().lower()
