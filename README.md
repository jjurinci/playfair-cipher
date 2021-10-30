# Playfair Cipher
The Playfair cipher was the first practical digraph substitution cipher. The scheme was invented in 1854 by Charles Wheatstone but was named after Lord Playfair who promoted the use of the cipher. In playfair cipher unlike traditional cipher we encrypt a pair of alphabets(digraphs) instead of a single alphabet.
It was used for tactical purposes by British forces in the Second Boer War and in World War I and for the same purpose by the Australians during World War II. This was because Playfair is reasonably fast to use and requires no special equipment.

## The Playfair Cipher Encryption Algorithm
***The algorithm consists of 2 steps:***
- *Generate the key table* - The key table is a **5×5** grid of alphabets that acts as the key for encrypting the plaintext. Each of the 25 alphabets must be unique and one letter of the alphabet (usually J) is omitted from the table (as the table can hold only 25 alphabets). If the plaintext contains J, then it is replaced by I. The initial alphabets in the key table are the unique alphabets of the key in the order in which they appear followed by the remaining letters of the alphabet in order
```python
CHAR_TO_OMIT = 'J'
CHAR_TO_REPLACE = 'I'
BOGUS_CHAR = 'X'
```
```python
def generate_table(key: str) -> list[str]:
    alphabet = string.ascii_uppercase.replace(CHAR_TO_OMIT, "")

    table = []

    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)

    for char in alphabet:
        if char not in table:
            table.append(char)

    return table
```

```python
def prepare_input(dirty: str) -> str:
    """
    Prepare the plaintext by up-casing it,
    separating repeated letters with X's and
    replacing all the J letters with I's
    """

    dirty = "".join([c.upper() for c in dirty if c in string.ascii_letters]).replace(
        CHAR_TO_OMIT, CHAR_TO_REPLACE)
    clean = ""

    if len(dirty) < 2:
        return dirty

    for i in range(len(dirty) - 1):
        clean += dirty[i]

        if dirty[i] == dirty[i + 1]:
            clean += BOGUS_CHAR

    clean += dirty[-1]

    if len(clean) & 1:
        clean += BOGUS_CHAR

    return clean
```
- *Algorithm to encrypt the plain text* - The plaintext is split into pairs of two letters (digraphs). If there is an odd number of letters, a bogus letter is added to the last letter. Pair cannot be made with same letter. Break the letter in single and add a bogus letter to the previous letter. If the letter is standing alone in the process of pairing, then add an extra bogus letter with the alone letter.
```python
def encode(plaintext: str, key: str) -> str:
    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    ciphertext = ""

    for char1, char2 in chunker(plaintext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)
```

***Rules for Encryption:***
- *If both the letters are in the same column* - Take the letter below each one (going back to the top if at the bottom)
```python
if row1 == row2:
    ciphertext += table[row1 * 5 + (col1 + 1) % 5]
    ciphertext += table[row2 * 5 + (col2 + 1) % 5]
```
- *If both the letters are in the same row* - Take the letter to the right of each one (going back to the leftmost if at the rightmost position)
```python
elif col1 == col2:
    ciphertext += table[((row1 + 1) % 5) * 5 + col1]
    ciphertext += table[((row2 + 1) % 5) * 5 + col2]
```
- *If neither of the above rules is true* - Form a rectangle with the two letters and take the letters on the horizontal opposite corner of the rectangle
```python
else:
    ciphertext += table[row1 * 5 + col2]
    ciphertext += table[row2 * 5 + col1]
```
## The Playfair Cipher Decryption Algorithm
***Decrypting the Playfair cipher is as simple as doing the same process in reverse. The receiver has the same key and can create the same key table, and then decrypt any messages made using that key. The algorithm consists of 2 steps:***
- *Generate the key table at the receiver's end* - The key table is a **5×5** grid of alphabets that acts as the key for encrypting the plaintext. Each of the 25 alphabets must be unique and one letter of the alphabet (usually J) is omitted from the table (as the table can hold only 25 alphabets). If the plaintext contains J, then it is replaced by I. The initial alphabets in the key table are the unique alphabets of the key in the order in which they appear followed by the remaining letters of the alphabet in order.

- *Algorithm to decrypt the ciphertext* - The ciphertext is split into pairs of two letters (digraphs). **The ciphertext always has an even number of characters.**
```python
def decode(ciphertext: str, key: str) -> str:
    table = generate_table(key)
    plaintext = ""

    for char1, char2 in chunker(ciphertext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)
```
***Rules for Decryption:***
- *If both the letters are in the same column* - Take the letter above each one (going back to the bottom if at the top)
```python
if row1 == row2:
    plaintext += table[row1 * 5 + (col1 - 1) % 5]
    plaintext += table[row2 * 5 + (col2 - 1) % 5]
```
- *If both the letters are in the same row* - Take the letter to the left of each one (going back to the rightmost if at the leftmost position)
```python
elif col1 == col2:
    plaintext += table[((row1 - 1) % 5) * 5 + col1]
    plaintext += table[((row2 - 1) % 5) * 5 + col2]

```
- *If neither of the above rules is true* - Form a rectangle with the two letters and take the letters on the horizontal opposite corner of the rectangle
```python
else:
    plaintext += table[row1 * 5 + col2]
    plaintext += table[row2 * 5 + col1]
```
# Brute force napad na playfair-ov sifrat

**Napomena:** napad nije optimiziran, ali probija playfair-ov šifrat ako mu se daju dobri parametri i ako ga se pokrene dovoljno puta (obicno 2-3). Također, zbog prethodnih neuspjelih implementacija napada (sporost) smo se inspirirali [ovim znanstvenim radom](https://ep.liu.se/ecp/158/010/ecp19158010.pdf) i [ovim java kodom](https://github.com/damiannolan/simulated-annealing-playfair-cipher-breaker/).

<br>
Kategorija napada: **Frequency attack (simulated annealing)**

### Simulated Annealing napad
[Simulated annealing (SA)](https://en.wikipedia.org/wiki/Simulated_annealing) je vjerojatnosna tehnika za aproksimaciju globalnog optimuma dane funkcije.

Za razliku od metoda kao što su hill climbing koji su lako smeteni lokalnim optimumom,
SA koristi randomizaciju da bi izašao iz lokalnih optimuma i nastavio aproksimirati globalni optimum.
To je jedan od razloga zašto je dosta efektivniji u razbijanju šifrata generiranih sa slučajnim ključevima.

**Input:** samo šifrat

**Bitne varijable: ** temperatura i tranzicije (mijenjanje temperature može znatno utjecati na rješenje)

**Optimizacijska funkcija:** suma log10 vjerojatnosti frekvencije quadgram-ova (string od 4 slova) plaintext-a. Pretpostavlja koliko je plaintext "engleski", što je više "engleski" to će plaintext dobiti bolju ocjenu.

**Izbjegavanje lokalnog optimuma:** prihvaćanje "neoptimalnijeg" rješenja sa vjerojatnošću od e^(difference/temperature) i nastavljanje traganja za globalnim optimumom

## Kako koristiti kod

### Direktno kao library

1. Klonirati ovaj repozitorij sa ```git clone https://github.com/jjurinci/playfair-cipher.git```
2. Postaviti svoj playfair-ov šifrat u datoteku (pr. sifrat.txt) i spremiti ju u direktorij **"data/encrypted_text"**
3. Napraviti python modul (pr. example.py) kopirati donji kod unutra
```python
from freq_attack import Attack

temperatura = 20
datoteka = "sifrat.txt"
napad = Attack(datoteka)
napad.brute_force(temperatura)
```

### ILI preko command-line interface-a
1. Klonirati ovaj repozitorij sa ```git clone https://github.com/jjurinci/playfair-cipher.git```
2. Postaviti svoj playfair-ov šifrat u datoteku (pr. sifrat.txt) i spremiti ju u direktorij **"data/encrypted_text"**
3. Preko terminala pokrenuti cmd_interface.py sa "python3 cmd_interface.py" i slijediti korake (potrebno imati numpy instaliran)
