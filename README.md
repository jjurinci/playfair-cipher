# Playfair Cipher
Playfair šifra bila je prva praktična supstitucijska šifra digrafa. Shemu je 1854. izumio Charles Wheatstone, ali je dobio ime po Lordu Playfairu koji je promovirao korištenje šifre. U playfair šifri, za razliku od tradicionalne šifre, šifriramo par slova (digrafa) umjesto jednog slova.
Koristile su ga u taktičke svrhe britanske snage u drugom burskom ratu i u prvom svjetskom ratu, a u istu svrhu i Australci tijekom drugog svjetskog rata. To je zato što je Playfair relativno brz za korištenje i ne zahtijeva posebnu opremu.

## The Playfair Cipher Encryption Algorithm
***The algorithm consists of 2 steps:***
- *Generiranje tablice ključa* - Tablica ključa je **5×5** matrica slova abecede koja služi kao ključ za enkriptiranje plaintext-a. Svako od 25 slova mora biti unikatno i jedno slovo se ispušta (obično J), zato što matrica ima kapacitet od samo 25 elemenata. Ako plaintext ima slovo J onda se zamjenjuje sa slovom I. Inicijalna slova u matrici su unikatna slova ključa (keyword), zatim ostatak unikatne abecede.
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
- *Algoritam za enkriptiranje plaintext-a* - Plaintext je podijeljen u parove od 2 slova (digrafi). Ako postoji neparan broj slova, posljednjem se slovu dodaje lažno (bogus) slovo. Par se ne može napraviti sa istim slovom. Ukoliko se to desi, digraf se razbija i lažno slovo se dodaje u sredinu. Ako slovo stoji samostalno u procesu uparivanja, dodaje mu se lažno slovo.
```python
def encode(plaintext: str, key: str) -> str:
    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    ciphertext = ""

    for char1, char2 in chunker(plaintext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)
```

***Pravila enkripcije:***
- *Ako su oba slova u istoj koloni* - Uzima se slovo ispod (promatranog slova) cirkularno (uzima se prvo gornje slovo ako ne postoji slovo ispod)
```python
if row1 == row2:
    ciphertext += table[row1 * 5 + (col1 + 1) % 5]
    ciphertext += table[row2 * 5 + (col2 + 1) % 5]
```
- *Ako su oba slova u istom redu* - Uzima se slovo desno (od promatranog slova) cirkularno (uzima se prvo lijevo slovo ako ne postoji desno slovo)
```python
elif col1 == col2:
    ciphertext += table[((row1 + 1) % 5) * 5 + col1]
    ciphertext += table[((row2 + 1) % 5) * 5 + col2]
```
- *Inače* - Formirati pravokutnik gdje su dijagonalno suprotni kutevi 2 promatrana slova. Za svako promatrano slovo se uzima slovo u horizontalnom suprotnom kutu pravokutnika.
```python
else:
    ciphertext += table[row1 * 5 + col2]
    ciphertext += table[row2 * 5 + col1]
```
## The Playfair Cipher Decryption Algorithm
***Dekripcija Playfair-ove šifre je jednostavno isti proces, ali unatrag. Primatlej ima isti ključ i kreira istu matricu, i zatim dekriptira bilo koji šifrat koji je napravljen s tim ključem. Algoritam se sastoji od 2 koraka:***
- *Generiranje tablice ključa (primatelj)* - Tablica ključa je **5×5** matrica slova abecede koja služi kao ključ za enkriptiranje plaintext-a. Svako od 25 slova mora biti unikatno i jedno slovo se ispušta (obično J), zato što matrica ima kapacitet od samo 25 elemenata. Ako plaintext ima slovo J onda se zamjenjuje sa slovom I. Inicijalna slova u matrici su unikatna slova ključa (keyword), zatim ostatak unikatne abecede.

- *Algoritam za dekriptiranje šifrata* - Šifrat se dijeli u parove od 2 slova (digraf). **Šifrat uvijek ima paran broj slova.**
```python
def decode(ciphertext: str, key: str) -> str:
    table = generate_table(key)
    plaintext = ""

    for char1, char2 in chunker(ciphertext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)
```
***Pravila dekripcije:***
- *Ako su oba slova u istoj koloni:* - Uzima se slovo iznad (promatranog slova) cirkularno (uzima se prvo donje slovo ako ne postoji slovo iznad)
```python
if row1 == row2:
    plaintext += table[row1 * 5 + (col1 - 1) % 5]
    plaintext += table[row2 * 5 + (col2 - 1) % 5]
```
- *Ako su oba slova u istom redu:* - Uzima se slovo lijevo (od promatranog slova) cirkularno (uzima se prvo desno slovo ako ne postoji lijevo slovo)
```python
elif col1 == col2:
    plaintext += table[((row1 - 1) % 5) * 5 + col1]
    plaintext += table[((row2 - 1) % 5) * 5 + col2]

```
- *Inače* - Formirati pravokutnik gdje su dijagonalno suprotni kutevi 2 promatrana slova. Za svako promatrano slovo se uzima slovo u horizontalnom suprotnom kutu pravokutnika.
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
