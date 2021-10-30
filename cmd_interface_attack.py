from freq_attack import Attack
from os import listdir, getcwd
from os.path import isfile, join

def cmd_interface():
    print("\n---------------------------------------------")
    print("| Simulated annealing brute force algoritam |")
    print("---------------------------------------------")
    print("NOTE: Zbog slucajnosti, da bi se osigurao uspjeh desifriranja\nalgoritam treba pokretati nekoliko puta sa istim ili\npromijenjenim parametrima.")
    print("---------------------------------------------")

    print("\nTrazim u: ./data/encrypted_text")
    current_path = getcwd() + "/data/encrypted_text"
    onlyfiles = [f for f in listdir(current_path) if isfile(join(current_path, f))]
    print("Pronasao datoteke: ", onlyfiles)

    while True:
        try:
            file = input("\nIme jedne od gornjih datoteka: ")
            attack = Attack(file)
            break
        except FileNotFoundError:
            print("Neispravna datoteka.")
        except KeyboardInterrupt:
            quit()

    print("---------------------------------------------")
    print("\nVarijabla temperatura znatno utjece na tocnost rjesenja.")
    print("\n\t10 \t- \t(do 500 slova)\n\t20 \t- \t(500 - 1000 slova)\n\tdrugo\t- \tvasa eksperimentacija")

    while True:
        try:
            temperature = input("\nTemperatura: ")
            temperature = int(temperature)
            break
        except ValueError:
            print("Neispravna temperatura.")
        except KeyboardInterrupt:
            quit()

    attack.brute_force(temperature, True)

if __name__ == "__main__":
    cmd_interface()
