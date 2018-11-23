import numpy as np
import math
import copy
from collections import deque


class NotFound(Exception): pass
np.set_printoptions(suppress=True, precision=3)


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0
        self.mat_c = np.array([])
        self.mat_b = np.array([])
        self.mat_a = np.array([])


ind_izrav_vr, ind_izrav_kol = 0, 0
iter = 1


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

    pom_mat = copy.copy(mat_cena.mat_c)

    # Biramo min iz matrice C i azuriramo vrednosti b i a u koloni/vrsti tog minimuma
    while len(np.where(mat_cena.mat_a != 0)[0]) != 0 and len(np.where(mat_cena.mat_c != 0)[0]) != 0:

        # Uzimamo prvi minimum ako ih ima vise
        minimumi = np.where(pom_mat == np.min(pom_mat))
        min_vr = minimumi[0][0]
        min_kol = minimumi[1][0]
        poten = min(mat_cena.mat_b[min_kol], mat_cena.mat_a[min_vr][0])

        mat_potencijala.mat_c[min_vr][min_kol] = poten

        if poten == mat_cena.mat_b[min_kol]:

            mat_cena.mat_b[min_kol] = 0
            mat_cena.mat_a[min_vr][0] -= poten
            pom_mat[:, min_kol] = 10000
        else:

            mat_cena.mat_a[min_vr][0] = 0
            mat_cena.mat_b[min_kol] -= poten
            pom_mat[min_vr, :] = 10000


def napravi_listu_povezanosti(pom):

    lista_pov = {}
    for i in range(pom.shape[0]):
        for j in range(pom.shape[1]):
            if pom[i][j] != 0:
                # Parnom broju gledamo samo susede u koloni
                if pom[i][j] % 2 == 0:
                    kol_susedi = [(k * 10 + j) for k in range(pom.shape[0]) if pom[k][j] != 0 and k != i]
                    lista_pov[i * 10 + j] = kol_susedi

                # Neparnom broju gledamo samo susede u vrsti
                else:
                    vr_susedi = [(i * 10 + k) for k in range(pom.shape[1]) if pom[i][k] != 0 and k != j]
                    lista_pov[i * 10 + j] = vr_susedi

    return lista_pov


def pretraga(graf, start, cilj):

    obidjen = {start: None}
    red = deque([start])
    while red:
        cvor = red.popleft()
        if cvor == cilj:
            put = []
            while cvor is not None:
                put.append(cvor)
                cvor = obidjen[cvor]
            return put[::-1]
        for susedni in graf[cvor]:
            if susedni not in obidjen:
                obidjen[susedni] = cvor
                red.append(susedni)


def pronadji_cikl(najneg_vr, najneg_kol, mat_potencijala):

    pom = np.zeros(mat_potencijala.mat_c.shape)
    pom[najneg_vr][najneg_kol] = 1
    mat_potencijala.mat_c[najneg_vr][najneg_kol] = 0
    obelezen = 1

    while 1:

        # Neparan pa idemo po vrstama
        if obelezen % 2 != 0:

            bazisne_vr = np.where(pom == obelezen)[0]
            if np.size(bazisne_vr) == 0:
                break

            for i in bazisne_vr:

                baz = np.where(mat_potencijala.mat_c[i] != 0)[0]
                for j in baz:

                    if len(np.where(baz == najneg_kol)[0]) and obelezen > 3:
                        break

                    if pom[i][j] == 0:
                        pom[i][j] = obelezen + 1

        # Paran pa idemo po kolonama
        else:

            bazisne_kol = np.where(pom == obelezen)[1]
            if np.size(bazisne_kol) == 0:
                break

            for j in bazisne_kol:
                baz = np.where(mat_potencijala.mat_c[:, j] != 0)[0]

                if len(np.where(baz == najneg_vr)[0]) and obelezen > 3:
                    break

                for t in baz:
                    if pom[t][j] == 0:
                        pom[t][j] = obelezen + 1

        obelezen += 1

    # Pravimo listu povezanosti
    lista_pov = napravi_listu_povezanosti(pom)
    start = najneg_vr * 10 + najneg_kol

    # Pronalazimo krajnji cvor koji ima za potomka koreni cvor
    cilj = 0
    for i in lista_pov:
        for j in lista_pov[i]:
            if j == start:
                cilj = i

    pozicije = pretraga(lista_pov, start, cilj)
    print("Najkraci put:", pozicije)

    znak = -1
    teta = np.zeros((pom.shape[0], pom.shape[1]))

    for poz in pozicije:
        znak *= -1
        i = int(poz / 10)
        j = poz % 10
        teta[i][j] = znak

    teta[najneg_vr][najneg_kol] = 1
    print("Teta, cikl:\n", teta)

    # Trazimo minimalno teta
    pot_min = np.array([])
    vrste, kolone = np.where(teta == -1)

    for i, j in zip(vrste, kolone):
        pot_min = np.append(pot_min, mat_potencijala.mat_c[i][j])

    teta_vr = min(pot_min)
    print("Teta min:", teta_vr)

    mat_potencijala.mat_c  = mat_potencijala.mat_c + teta * teta_vr
    print("Nova matrica potencijala:\n", mat_potencijala.mat_c)
    return mat_potencijala.mat_c


def metod_potencijala(mat_cena, mat_potencijala):

    global iter
    print("Iteracija:", iter)
    max_bazisnih_vr = 0
    max_bazisnih_kol = 0
    vrsta_max = 0
    kolona_max = 0
    mat_potencijala.mat_b = np.repeat(float('-inf'), mat_potencijala.br_kolona)
    mat_potencijala.mat_a = np.repeat(float('-inf'), mat_potencijala.br_vrsta) \
        .reshape((mat_potencijala.br_vrsta, 1))

    # Trazimo vrstu sa najvise bazisnih promenljivih
    for i, linija in enumerate(mat_potencijala.mat_c):
        br_bazisnih = np.size(np.where(linija != 0)[0])
        if br_bazisnih > max_bazisnih_vr:
            max_bazisnih_vr = br_bazisnih
            vrsta_max = i

    # Trazimo kolonu sa najvise bazisnih promenljivih
    for j, kolona in enumerate(mat_potencijala.mat_c.T):
        br_bazisnih = np.size(np.where(kolona != 0)[0])
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

                bazisne = np.where(mat_potencijala.mat_c[r] != 0)[0]
                for m in bazisne:
                    mat_potencijala.mat_b[m] = mat_cena.mat_c[r][m] - mat_potencijala.mat_a[r][0]

        # Prolazimo kolone i radimo isto samo sto gledamo B,a upisujemo u A rezultat cijB - Bi
        for r, broj in enumerate(mat_potencijala.mat_b):
            if broj != float('-inf'):

                nove_bazisne = np.where(mat_potencijala.mat_c[:, r] != 0)[0]
                for m in nove_bazisne:
                    mat_potencijala.mat_a[m][0] = mat_cena.mat_c[m][r] - mat_potencijala.mat_b[r]

    print("Matrice nakon popunjavanja B, A:\n")
    ispis(mat_cena)
    ispis(mat_potencijala)

    indikator = 0
    tren_najneg = float('+inf')
    najnegativniji = 0
    najneg_vr = 0
    najneg_kol = 0

    # Proveravamo ispunjenost uslova cijN - (Ai + Bj) >= 0
    for i, vrsta in enumerate(mat_potencijala.mat_c):
        for j, vr_c in enumerate(vrsta):

            raz = mat_cena.mat_c[i][j] - (mat_potencijala.mat_b[j] + mat_potencijala.mat_a[i][0])
            if vr_c == 0 and raz < 0:

                indikator = 1
                if raz < tren_najneg:

                    najneg_vr = i
                    najneg_kol = j
                    najnegativniji = mat_cena.mat_c[i][j]
                    tren_najneg = raz

    # Racunamo optimalno resenje
    if indikator == 0:

        # Brisemo izravnavajucu vrst/kolonu ako je dodata
        if ind_izrav_vr == 1:
            mat_potencijala.mat_c = np.delete(mat_potencijala.mat_c, -1, axis=0)
        elif ind_izrav_kol == 1:
            mat_potencijala.mat_c = np.delete(mat_potencijala.mat_c, -1, axis=1)

        konacna_suma = 0
        for i, vrsta in enumerate(mat_potencijala.mat_c):
            for j, vr_c in enumerate(vrsta):

                if vr_c != 0:
                    konacna_suma += vr_c * mat_cena.mat_c[i][j]

        print("Optimalno resenje:", konacna_suma)
        exit()

    mat_potencijala.mat_c = pronadji_cikl(najneg_vr, najneg_kol, mat_potencijala)

    iter += 1
    return metod_potencijala(mat_cena, mat_potencijala)


def main():

    global ind_izrav_kol, ind_izrav_vr
    mat_cena = Sistem()
    unesiUlaz(mat_cena)

    # Ako je sumaB != sumaA dodajemo vrstu/kolonu i razliku u mat_b/mat_a, kako bi izjednacili
    razlika = sum(mat_cena.mat_b) - sum(mat_cena.mat_a)
    if razlika > 0:

        ind_izrav_vr = 1
        mat_cena.br_vrsta += 1
        mat_cena.mat_c = np.append(mat_cena.mat_c, [np.repeat(50, mat_cena.br_kolona)], axis=0)
        mat_cena.mat_a = np.append(mat_cena.mat_a, [razlika], axis=0)

    elif razlika < 0:

        ind_izrav_kol = 1
        mat_cena.br_kolona += 1
        print(mat_cena.mat_c, [np.repeat(50, mat_cena.br_vrsta)])
        mat_cena.mat_c = np.append(mat_cena.mat_c, np.repeat(50, mat_cena.br_vrsta)
                                   .reshape(mat_cena.br_vrsta, 1), axis=1)
        mat_cena.mat_b = np.append(mat_cena.mat_b, -razlika)

    # Pravimo matricu potencijala, na pocetno (sve -inf)
    mat_potencijala = Sistem()
    mat_potencijala.br_vrsta = mat_cena.br_vrsta
    mat_potencijala.br_kolona = mat_cena.br_kolona

    mat_potencijala.mat_c = np.repeat(0, mat_potencijala.br_vrsta * mat_potencijala.br_kolona)\
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


if __name__ == '__main__':
    main()