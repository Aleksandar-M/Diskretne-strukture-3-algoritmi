import numpy as np
import copy

np.set_printoptions(suppress=True, precision=3)


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0  # rezultat funkcije!
        self.problem = ""
        self.koefs_problema = np.array([])
        self.niz_znakova = np.array([])
        self.matricaA = np.array([])
        self.matricaB = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])


# Funkcija za unos
def unesiUlaz(s):
    funkcija = input("Unesite problem ( u obliku max ili min) i koeficijente funkcije:").split(" ")

    if funkcija[0] == "max" or funkcija[0] == "min":
        s.problem = str(funkcija[0])
    else:
        print("\n Pogresan unos problema.")
        exit()

    s.koefs_problema = np.array(list(map(float, funkcija[1:])))

    ulaz = input("Unesite broj nejednacina i broj nepoznatih, NE racunajuci podrazumevane x1>=0...):")

    s.br_vrsta = int(ulaz.split(" ")[0])
    s.br_kolona = int(ulaz.split(" ")[1])

    s.matricaA = np.zeros((s.br_vrsta, s.br_kolona))
    s.matricaB = np.zeros((s.br_vrsta, 1))

    for i in range(s.br_vrsta):

        linija = input("Unesite sve koeficijente nejednacine kao i znak:").split(" ")
        s.niz_znakova = np.append(s.niz_znakova, linija[-2])
        koefs_nejednacine = list(map(float, linija[:-2] + linija[-1:]))
        duzina = len(koefs_nejednacine)

        for j in range(duzina):
            if j == duzina - 1:
                s.matricaB[i][0] = koefs_nejednacine[j]
            else:
                s.matricaA[i][j] = koefs_nejednacine[j]

    print("niz znakova", len(s.niz_znakova))

# Funkcija za svodjenje na kanonski oblik
def kanonskiOblik(s):
    j = s.br_kolona

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        #s.problem = "min"
        s.koefs_problema *= (-1)

    for i in range(s.br_kolona):
        s.Q = np.append(s.Q, i)

    # Prebacujemo nejednacine u jednacine
    for i in range(s.br_vrsta):

        if s.niz_znakova[i] != "=":

            nule = np.zeros((s.br_vrsta, 1))

            if s.niz_znakova[i] == ">=":
                nule[i][0] = -1
            elif s.niz_znakova[i] == "<=":
                nule[i][0] = 1

            s.matricaA = np.append(s.matricaA, nule, axis=1)
            s.niz_znakova[i] = "="
            s.br_kolona += 1  # Izmenjen broj kolona
            if nule[i][0] == 1:
                s.P = np.append(s.P, j)
            elif nule[i][0] == -1:
                s.Q = np.append(s.Q, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    s.koefs_problema = np.append(s.koefs_problema, np.zeros((1, s.br_kolona - len(s.koefs_problema))))


# Pomocna funkcija za proveru uslova
def proveriUslov(koefs):
    for i in range(len(koefs)):
        if koefs[i] < 0:
            return False

    return True


# Pomocna funkcija za pronalazenje indeksa
def pronadjiIndeks(koefs, s):
    for i in range(len(koefs)):
        if koefs[i] < 0:
            return s.Q[i]


def ispis(s2):

    mat = s2.matricaA
    mat2 = s2.matricaB

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print('{: 3.2f}'.format(mat[i][j]), end=" ")
        print('{: 3.2f}'.format(mat2[i][0]))

    for i in range(len(s2.koefs_problema)):
        print('{: 3.2f}'.format(s2.koefs_problema[i]), end=" ")
    print(s2.rez_funkcije)

    print("-----------------")


# Pomocna funkcija za lep ispis matrice
# def ispisiMatricu(mat, mat2):
#
#     for i in range(len(mat)):
#         print(mat[i], mat2[i])
#
#
#     # for vrsta in mat:
#     #     for kolona in vrsta:
#     #         if kolona >= 0:
#     #             print(" ", round(kolona, 3), sep="", end=" ")
#     #         else:
#     #             print(round(kolona, 3), end=" ")
#     #
#     #     print("")
#     # print("")


def tablicni_simpleks(s):

    iteracija = 1

    while iteracija < 100:
        print("Iteracija:", iteracija)

        for k in range(len(s.matricaB)):
            if s.matricaB[k] < 0:

                # Provera da li su svi a-ovi pozitivni; ako T -> neogranicen problem
                br_poz = 0
                for m in range(s.br_kolona):
                    if s.matricaA[k][m] < 0:
                        break
                    else:
                        br_poz += 1

                if br_poz == s.br_kolona:
                    print("Neogranicen problem")
                    exit()

                # Trazimo pivot
                max = -100
                pivot_vrsta = 50
                pivot_kolona = 50
                pivot_vrednost = 50

                for i in range(s.br_kolona):
                    if s.matricaA[k][i] < 0:
                        nova_vr = s.koefs_problema[i] / s.matricaA[k][i]

                        # Trenutni max
                        if max <= nova_vr:     # Bez koriscenje pravila
                        # if max < nova_vr:    # Koriscenjem Blendovog pravila
                            max = nova_vr
                            pivot_vrsta = k
                            pivot_kolona = i
                            pivot_vrednost = s.matricaA[k][i]

                print("Pivot (vrsta, kolona, vrednost):", pivot_vrsta, pivot_kolona, pivot_vrednost)

                # Obavljamo elementarne transformacije nad ostalim vrstama - vrsimo pivotiranje
                for i in range(s.br_vrsta):

                    if i != pivot_vrsta:

                        stara_pivot_kolona = s.matricaA[i][pivot_kolona]
                        s.matricaA[i] = s.matricaA[i] + (-1)*stara_pivot_kolona/pivot_vrednost*s.matricaA[pivot_vrsta]
                        s.matricaB[i] = s.matricaB[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaB[pivot_vrsta]

                    stara_pivot_kolona_c = s.koefs_problema[pivot_kolona]
                    s.koefs_problema = s.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaA[pivot_vrsta]
                    s.rez_funkcije = s.rez_funkcije + (-1)*stara_pivot_kolona_c/pivot_vrednost * s.matricaB[pivot_vrsta]

                # Delimo celu vrstu sa trenutnim pivotom
                if pivot_vrednost != 0:

                    s.matricaA[pivot_vrsta] = s.matricaA[pivot_vrsta] / pivot_vrednost
                    s.matricaB[pivot_vrsta] = s.matricaB[pivot_vrsta] / pivot_vrednost

                break

        ispis(s)

        # Proveravamo da li su svi b-ovi nenegativni; ako T -> nasli smo optimalno resenje
        br_pozitivnih = 0

        for i in range(len(s.matricaB)):
            if s.matricaB[i] >= 0:
                br_pozitivnih += 1

        # Ispisujemo optimalno i vrednost funkcije
        if br_pozitivnih == len(s.matricaB):

            # Pronalazenje optimalnog resenja
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):

                jedinice = np.where(s.matricaA[:, i] == 1)[0]
                nule =  np.where(s.matricaA[:, i] == 0)[0]

                if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1:
                    opt_resenje[i] = s.matricaB[jedinice[0]]

            if s.problem == "min":
                print("\nmin f:", s.rez_funkcije[0]*(-1))
            else:
                print("\nmax f:", s.rez_funkcije[0])

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.2f}'.format(opt_resenje[i]), end=" ")
            print("")

            return

        iteracija += 1


def main():

    s = Sistem()
    unesiUlaz(s)
    print("Ulaz:\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.niz_znakova)
    ispis(s)

    # Ako je bila nejednacina oblika >= hocemo <=
    for i in range(s.br_vrsta):
        if s.niz_znakova[i] == ">=":
            s.matricaB[i] *= -1
            s.matricaA[i] *= -1
            s.niz_znakova[i] = "<="

    kanonskiOblik(s)
    print("U kanonskom obliku:\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.niz_znakova)
    ispis(s)

    tablicni_simpleks(s)


if __name__ == '__main__':
    main()
