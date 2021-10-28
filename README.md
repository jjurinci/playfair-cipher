# Opis Playfair-ovog šifrata
- To be done

# Brute force napad na playfair-ov sifrat

**Napomena:** napad nije optimiziran, ali probija playfair-ov šifrat ako mu se daju dobri parametri i ako ga se pokrene dovoljno puta (obicno 2-3). Također, zbog prethodnih neuspjelih implementacija napada (sporost) smo se inspirirali [ovim znanstvenim radom](https://ep.liu.se/ecp/158/010/ecp19158010.pdf) i [ovim java kodom](https://github.com/damiannolan/simulated-annealing-playfair-cipher-breaker/).

Jezik: **Python**
<br>
Kategorija napada: **Frequency attack (simulated annealing)**

###Simulated Annealing napad
[Simulated annealing (SA)](https://en.wikipedia.org/wiki/Simulated_annealing) je vjerojatnosna tehnika za aproksimaciju globalnog optimuma dane funkcije.

Za razliku od metoda kao što su hill climbing koji su lako smeteni lokalnim optimumom,
SA koristi randomizaciju da bi izašao iz lokalnih optimuma i nastavio aproksimirati globalni optimum.
To je jedan od razloga zašto je dosta efektivniji u razbijanju šifrata generiranih sa slučajnim ključevima.

**Input:** samo šifrat

**Bitne varijable: ** temperatura i tranzicije (mijenjanje temperature može znatno utjecati na rješenje)

**Optimizacijska funkcija: ** suma log10 vjerojatnosti frekvencije quadgram-ova (string od 4 slova) plaintext-a. Pretpostavlja koliko je plaintext "engleski", što je više "engleski" to će plaintext dobiti bolju ocjenu.

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
3. Preko terminala pokrenuti cmd interface sa python cmd_interface.py" i slijediti korake (potrebno imati numpy instaliran)
