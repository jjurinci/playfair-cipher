import numpy as np
import string

def clean(plaintext):
    plaintext = "".join([c.upper() for c in plaintext if c in string.ascii_letters]).replace("J", "I")
    clean = ""

    if len(plaintext) < 2:
        return plaintext

    for i in range(len(plaintext)-1):
        clean += plaintext[i]
        if plaintext[i] == plaintext[i+1]:
            clean += "X"

    clean += plaintext[-1]

    if len(clean) % 2:
        clean += "X"

    pairs_plaintext = []
    for index in range(0, len(clean), 2):
        pairs_plaintext.append((clean[index], clean[index+1]))

    return pairs_plaintext


def get_matrix(key):
    no_j_alphabet = string.ascii_uppercase.replace("J", "")
    key = key.upper() + no_j_alphabet

    # Removes duplicate characters (preserves order)
    key = ''.join(sorted(set(key), key=key.index))
    matrix = np.array(list(key)).reshape(5,5)
    return matrix


def encrypt(plaintext: str, key: str) -> str:
    assert len(key) <= 25, "Key length must be lesser or equal to 25."
    assert all(char in string.ascii_letters for char in key), "Key must consist of alphabet only"

    pairs_plaintext = clean(plaintext)
    matrix = get_matrix(key)

    ciphertext = ""
    for letter1, letter2 in pairs_plaintext:
        result1 = np.where(matrix == letter1)
        result2 = np.where(matrix == letter2)
        row1, col1 = result1[0][0], result1[1][0]
        row2, col2 = result2[0][0], result2[1][0]

        if row1 == row2:
            ciphertext += matrix[row1][(col1+1)%5]
            ciphertext += matrix[row2][(col2+1)%5]

        elif col1 == col2:
            ciphertext += matrix[(row1+1)%5][col1]
            ciphertext += matrix[(row2+1)%5][col2]

        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext

def decrypt(ciphertext, key):
    pairs_ciphertext = []
    for index in range(0, len(ciphertext), 2):
        pairs_ciphertext.append((ciphertext[index], ciphertext[index+1]))

    matrix = get_matrix(key)

    plaintext = ""
    for letter1, letter2 in pairs_ciphertext:
        result1 = np.where(matrix == letter1)
        result2 = np.where(matrix == letter2)
        row1, col1 = result1[0][0], result1[1][0]
        row2, col2 = result2[0][0], result2[1][0]

        if row1 == row2:
            plaintext += matrix[row1][(col1-1)%5]
            plaintext += matrix[row2][(col2-1)%5]

        elif col1 == col2:
            plaintext += matrix[(row1-1)%5][col1]
            plaintext += matrix[(row2-1)%5][col2]

        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return plaintext


encrypted = encrypt("Ovo je moja recenica! Dodajem jos malo znakova,!", "keyword")
decrypted = decrypt(encrypted, "keyword")
print(encrypted, decrypted)
