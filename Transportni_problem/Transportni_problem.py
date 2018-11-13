import numpy as np
import math
import copy

np.set_printoptions(suppress=True, precision=3)


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0
        self.mat_c = np.array([])
        self.mat_b = np.array([])
        self.mat_a = np.array([])


# Funkcija za unos
def unesiUlaz(s):

    ulaz = input("Unesite broj vrsta i kolona za C:").split(" ")

    s.br_vrsta = int(ulaz[0])
    s.br_kolona = int(ulaz[1])
    s.mat_c = np.zeros((s.br_vrsta, s.br_kolona))

    for i in range(s.br_vrsta):
        s.mat_c[i] = input("Unesite vrednosti vrste za C:").split(" ")

    s.mat_c = s.mat_c.astype(int)

    s.mat_a = np.array(input("Unesite vrednosti kolone za A:").split(" ")).reshape((s.br_vrsta, 1))
    s.mat_a = s.mat_a.astype(int)

    s.mat_b = np.array(input("Unesite vrednosti kolone za B:").split(" "))
    s.mat_b = s.mat_b.astype(int)


def ispis(s2):

    mat = s2.mat_a
    mat2 = s2.mat_c

    for i in range(len(mat2)):
        for j in range(len(mat2[0])):
            print('{: 4}'.format(mat2[i][j]), end=" ")
        print('{: 4}'.format(mat[i][0]))

    for i in range(s2.br_kolona):
        print('{: 4}'.format(s2.mat_b[i]), end=" ")

    print("\n-----------------")


def metod_min_cena(mat_cena, mat_potencijala):

    print(len(np.where(mat_cena.mat_b != 0)[0]))
    pom_mat = copy.copy(mat_cena.mat_c)

    # Biramo min iz matrice C i azuriramo vrednosti b i a u koloni/vrsti tog minimuma
    while len(np.where(mat_cena.mat_a != 0)[0]) != 0 and len(np.where(mat_cena.mat_c != 0)[0]) != 0:

        print(len(np.where(mat_cena.mat_b != 0)[0]))
        print(len(np.where(mat_cena.mat_a != 0)[0]))

        print(pom_mat)

        # Uzimamo prvi minimum ako ih ima vise
        minimumi = np.where(pom_mat == np.min(pom_mat))
        min_vr = minimumi[0][0]
        min_kol = minimumi[1][0]
        print("minimum", np.min(pom_mat), min_vr, min_kol)

        poten = min(mat_cena.mat_b[min_kol], mat_cena.mat_a[min_vr][0])
        print(poten, mat_cena.mat_b[min_kol], mat_cena.mat_a[min_vr][0])

        mat_potencijala.mat_c[min_vr][min_kol] = poten

        if poten == mat_cena.mat_b[min_kol]:
            mat_cena.mat_b[min_kol] = 0
            mat_cena.mat_a[min_vr][0] -= poten
            pom_mat[:, min_kol] = 10000                                 #magicna promenljiva
        else:
            mat_cena.mat_a[min_vr][0] = 0
            mat_cena.mat_b[min_kol] -= poten
            pom_mat[min_vr, :] = 10000


        print(pom_mat)

        ispis(mat_cena)
        ispis(mat_potencijala)

    #### provera m+n-1

    ispis(mat_cena)
    ispis(mat_potencijala)


def metod_potencijala(mat_cena, mat_potencijala):

    max_bazisnih_vr = 0
    max_bazisnih_kol = 0
    vrsta_max = 0
    kolona_max = 0

    # Trazimo vrstu sa najvise bazisnih promenljivih
    for i, linija in enumerate(mat_potencijala.mat_c):
        br_bazisnih = np.size(np.where(linija != float('-inf'))[0])
        if br_bazisnih > max_bazisnih_vr:
            max_bazisnih_vr = br_bazisnih
            vrsta_max = i

    # Trazimo kolonu sa najvise bazisnih promenljivih
    for j, kolona in enumerate(mat_potencijala.mat_c.T):
        br_bazisnih = np.size(np.where(kolona != float('-inf'))[0])
        if br_bazisnih > max_bazisnih_kol:
            max_bazisnih_kol = br_bazisnih
            kolona_max = j

    # Za pocetnu biramo vrstu ili kolonu sa najvise bazisnih promenljivih
    if max_bazisnih_vr >= max_bazisnih_kol:
        mat_potencijala.mat_a[vrsta_max][0] = 0
    else:
        mat_potencijala.mat_b[kolona_max] = 0

    # Racunamo dok sva polja iz B i A ne popunimo
    while np.size(np.where(mat_potencijala.mat_b == float('-inf'))[0]) > 0 \
            or np.size(np.where(mat_potencijala.mat_a == float('-inf'))[0]) > 0:

        # Prolazimo vrste i gde je je uneta vrednost u A u toj vrsti trazimo bazisne i za njihove kolone
        # zatim u B upisujemo rezultat cijB - Ai
        for r, broj in enumerate(mat_potencijala.mat_a):
            if broj != float('-inf'):

                bazisne = np.where(mat_potencijala.mat_c[r] != float('-inf'))[0]
                for m in bazisne:
                    mat_potencijala.mat_b[m] = mat_cena.mat_c[r][m] - mat_potencijala.mat_a[r][0]

        # Prolazimo kolone i radimo isto samo sto gledamo B,a upisujemo u A rezultat cijB - Bi
        for r, broj in enumerate(mat_potencijala.mat_b):
            if broj != float('-inf'):

                nove_bazisne = np.where(mat_potencijala.mat_c[:, r] != float('-inf'))[0]
                for m in nove_bazisne:
                    mat_potencijala.mat_a[m][0] = mat_cena.mat_c[m][r] - mat_potencijala.mat_b[r]


def main():

    mat_cena = Sistem()
    unesiUlaz(mat_cena)

    # Ako je sumaB != sumaA dodajemo vrstu/kolonu i razliku u mat_b/mat_a, kako bi izjednacili
    razlika = sum(mat_cena.mat_b) - sum(mat_cena.mat_a)
    if razlika > 0:

        mat_cena.br_vrsta += 1
        mat_cena.mat_c = np.append(mat_cena.mat_c, [np.repeat(50, mat_cena.br_kolona)], axis=0)
        mat_cena.mat_a = np.append(mat_cena.mat_a, [razlika], axis=0)

    elif razlika < 0:

        mat_cena.br_kolona += 1
        print(mat_cena.mat_c, [np.repeat(50, mat_cena.br_vrsta)])
        mat_cena.mat_c = np.append(mat_cena.mat_c, np.repeat(50, mat_cena.br_vrsta)
                                   .reshape(mat_cena.br_vrsta, 1), axis=1)
        mat_cena.mat_b = np.append(mat_cena.mat_b, -razlika)

    # Pravimo matricu potencijala, na pocetno (sve -inf)
    mat_potencijala = Sistem()
    mat_potencijala.br_vrsta = mat_cena.br_vrsta
    mat_potencijala.br_kolona = mat_cena.br_kolona

    mat_potencijala.mat_c = np.repeat(float('-inf'), mat_potencijala.br_vrsta * mat_potencijala.br_kolona)\
        .reshape((mat_potencijala.br_vrsta, mat_potencijala.br_kolona))
    mat_potencijala.mat_b = np.repeat(float('-inf'), mat_potencijala.br_kolona)
    mat_potencijala.mat_a = np.repeat(float('-inf'), mat_potencijala.br_vrsta)\
        .reshape((mat_potencijala.br_vrsta, 1))

    print("\n")
    ispis(mat_cena)
    ispis(mat_potencijala)

    metod_min_cena(mat_cena, mat_potencijala)
    print("Matrice nakon metoda minimalnih cena:\n")
    ispis(mat_cena)
    ispis(mat_potencijala)

    metod_potencijala(mat_cena, mat_potencijala)
    print("Matrice nakon metoda potencijala:\n")
    ispis(mat_cena)
    ispis(mat_potencijala)


if __name__ == '__main__':
    main()