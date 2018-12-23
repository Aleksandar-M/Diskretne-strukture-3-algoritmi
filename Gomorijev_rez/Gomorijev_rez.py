from builtins import print

import numpy as np
import copy
import math

#np.set_printoptions(suppress=False, precision=3)


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = np.array([0])  # rezultat funkcije!
        self.problem = ""
        self.koefs_problema = np.array([])
        self.niz_znakova = np.array([])
        self.matricaA = np.array([])
        self.matricaB = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])

        self.baz_prom = 0

blend = "da"


# Funkcija za unos
def unesiUlaz(s):
    global blend
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

    s.baz_prom = int(ulaz.split(" ")[1])

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

    blend = input("Unesite da/ne za koriscenje Blendovog pravila")
    print("niz znakova", len(s.niz_znakova))


# Funkcija za svodjenje na kanonski oblik
def kanonskiOblik(s):
    j = s.br_kolona

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        # s.problem = "min"
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
            print('{: f}'.format(mat[i][j]), end=" ")
        print('{: f}'.format(mat2[i][0]))

    for i in range(len(s2.koefs_problema)):
        print('{: 3f}'.format(s2.koefs_problema[i]), end=" ")
    print(s2.rez_funkcije)

    print("-----------------")


# Pomocna funkcija za obavljanje elementarnih transfomacija nad matricom
def elem_transformacije(s2, pivot_vrsta, pivot_kolona, pivot_vrednost):
    for k in range(s2.br_vrsta):

        if k != pivot_vrsta:
            stara_pivot_kolona = s2.matricaA[k][pivot_kolona]
            s2.matricaA[k] = s2.matricaA[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaA[
                pivot_vrsta]
            s2.matricaB[k] = s2.matricaB[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaB[
                pivot_vrsta]

        stara_pivot_kolona_c = s2.koefs_problema[pivot_kolona]
        s2.koefs_problema = s2.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaA[
            pivot_vrsta]
        s2.rez_funkcije = s2.rez_funkcije + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaB[
            pivot_vrsta]

        # Ako je decimalni deo manji od 0.01 zaokruzujemo na ceo broj
        zaokruzi(s2)

    # Delimo celu vrstu sa trenutnim pivotom
    if pivot_vrednost != 0:
        s2.matricaA[pivot_vrsta] = s2.matricaA[pivot_vrsta] / pivot_vrednost
        s2.matricaB[pivot_vrsta] = s2.matricaB[pivot_vrsta] / pivot_vrednost

        zaokruzi(s2)


# Pomocna funkcija za transformisanje koeficijenata ispod bazisnih kolona
def ciscenje_koefs_problema(s3):
    for i in range(s3.br_kolona):

        jedinice = np.where(s3.matricaA[:, i] == 1)[0]
        nule = np.where(s3.matricaA[:, i] == 0)[0]

        if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:

            stari_koef = s3.koefs_problema[i]
            if stari_koef != 0:
                indeks_1 = jedinice[0]
                #print(s3.matricaA)
                #print(s3.koefs_problema, stari_koef, s3.matricaA[indeks_1, :])
                s3.koefs_problema = s3.koefs_problema + (-1) * stari_koef * s3.matricaA[indeks_1, :]
                s3.rez_funkcije = s3.rez_funkcije + (-1) * stari_koef * s3.matricaB[indeks_1, :]

        ispis(s3)


def tablicni_simpleks(s):
    iteracija = 1

    while iteracija < 300:
        print("Iteracija:", iteracija)

        for k in range(len(s.koefs_problema)):

            if s.koefs_problema[k] < 0:

                # Provera da li su svi iznad c negativni; ako je T -> neogranicen problem
                br_negativnih = 0
                for m in range(s.br_vrsta):
                    if s.matricaA[m][k] >= 0:
                        break
                    else:
                        br_negativnih += 1

                if br_negativnih == s.br_vrsta:
                    print("Neogranicen problem")
                    exit()

                # Trazimo pivot
                min = 100
                pivot_vrsta = 30
                pivot_kolona = 30
                pivot_vrednost = 30
                for i in range(s.br_vrsta):
                    if s.matricaA[i][k] > 0:
                        nova_vr = s.matricaB[i][0] / s.matricaA[i][k]

                        # Trenutni min
                        if blend == "da":
                            if min > nova_vr:  # Koriscenjem Blendovog pravila
                                min = nova_vr
                                pivot_vrsta = i
                                pivot_kolona = k
                                pivot_vrednost = s.matricaA[i][k]
                        else:
                            if min >= nova_vr:  # Bez koriscenja pravila
                                min = nova_vr
                                pivot_vrsta = i
                                pivot_kolona = k
                                pivot_vrednost = s.matricaA[i][k]

                elem_transformacije(s, pivot_vrsta, pivot_kolona, pivot_vrednost)
                break

        ispis(s)

        # Proveravamo da li su svi c-ovi nenegativni; ako T -> nasli smo optimalno resenje
        br_pozitivnih = 0
        for i in range(len(s.koefs_problema)):
            if s.koefs_problema[i] >= 0:
                br_pozitivnih += 1

        # Ispisujemo optimalno i vrednost funkcije
        if br_pozitivnih == len(s.koefs_problema):

            # pronalazenje optimalnog resenja
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):

                jedinice = np.where(s.matricaA[:, i] == 1)[0]
                nule = np.where(s.matricaA[:, i] == 0)[0]

                if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1:
                    opt_resenje[i] = s.matricaB[jedinice[0]]

            print("\nKorisceno Blendovo pravilo:", blend)

            if np.size(np.where(opt_resenje[:s.baz_prom] < 0)[0]) > 0:
                print("Nema dopustivih tacaka", opt_resenje[:s.baz_prom])
                exit()

            if s.problem == "min":
                print("min f:", s.rez_funkcije[0] * (-1))
            else:
                print("max f:", s.rez_funkcije[0])

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.2f}'.format(opt_resenje[i]), end=" ")
            print("")
            return

        iteracija += 1


def dualni_simpleks(s):
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
                pivot_vrsta = 30
                pivot_kolona = 30
                pivot_vrednost = 30

                for i in range(s.br_kolona):
                    if s.matricaA[k][i] < 0:
                        nova_vr = s.koefs_problema[i] / s.matricaA[k][i]

                        # Trenutni max
                        if blend == "da":
                            if max < nova_vr:  # Koriscenjem Blendovog pravila
                                max = nova_vr
                                pivot_vrsta = k
                                pivot_kolona = i
                                pivot_vrednost = s.matricaA[k][i]

                        else:
                            if max <= nova_vr:  # Bez koriscenje pravila
                                max = nova_vr
                                pivot_vrsta = k
                                pivot_kolona = i
                                pivot_vrednost = s.matricaA[k][i]

                print("Pivot (vrsta, kolona, vrednost):", pivot_vrsta, pivot_kolona, pivot_vrednost, "\n")

                # Obavljamo elementarne transformacije nad ostalim vrstama - vrsimo pivotiranje
                for i in range(s.br_vrsta):

                    if i != pivot_vrsta:
                        stara_pivot_kolona = s.matricaA[i][pivot_kolona]
                        s.matricaA[i] = s.matricaA[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaA[
                            pivot_vrsta]
                        s.matricaB[i] = s.matricaB[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaB[
                            pivot_vrsta]

                    stara_pivot_kolona_c = s.koefs_problema[pivot_kolona]
                    s.koefs_problema = s.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaA[
                        pivot_vrsta]
                    s.rez_funkcije = s.rez_funkcije + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaB[
                        pivot_vrsta]

                    # Zaokruzujemo sve vrednosti na dve decimale
                    zaokruzi(s)

                # Delimo celu vrstu sa trenutnim pivotom
                if pivot_vrednost != 0:
                    s.matricaA[pivot_vrsta] = s.matricaA[pivot_vrsta] / pivot_vrednost
                    s.matricaB[pivot_vrsta] = s.matricaB[pivot_vrsta] / pivot_vrednost

                    zaokruzi(s)

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
                nule = np.where(s.matricaA[:, i] == 0)[0]

                if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1:
                    opt_resenje[i] = s.matricaB[jedinice[0]]

            print("\nKorisceno Blendovo pravilo:", blend)

            # Ako je neko od resenja negativno
            if np.size(np.where(opt_resenje[:s.baz_prom] < 0)[0]) > 0:
                print("Nema dopustivih tacaka", opt_resenje[:s.baz_prom])
                exit()

            if s.problem == "min":
                print("min f:", np.round(s.rez_funkcije[0], 5) * (-1))
            else:
                print("max f:", np.round(s.rez_funkcije[0], 5))

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.2f}'.format(opt_resenje[i]), end=" ")
            print("")
            return

        iteracija += 1


# Pomocna fja za proveru postojanja negativnih c-ova
def negativni_c(s):

    c_ovi = s.koefs_problema
    for c in c_ovi:
        if c < 0:
            return True

    return False


# Pomocna fja za proveru postojanja negativnih b-ova
def negativni_b(s):

    b_ovi = s.matricaB
    for b in b_ovi:
        if b[0] < 0:
            return True

    return False


# Ako je decimalni deo manji od 0.01 zaokruzujemo na ceo broj
def zaokruzi(s):

    z = 10
    for i, lin in enumerate(s.matricaA):
        for j, vr in enumerate(lin):
            s.matricaA[i][j] = round(vr, z) + 0

    for i, vr in enumerate(s.matricaB):
        s.matricaB[i][0] = round(vr[0], z) + 0

    for i, vr in enumerate(s.koefs_problema):
        s.koefs_problema[i] = round(vr, z) + 0

    s.rez_funkcije = np.round(s.rez_funkcije, z) + 0
    return s


# Pomocna fja za proveru postojanja pocetne baze
def postoji_baza(s):

    bazisne_kol = 0

    for i, vr in enumerate(s.matricaA.T):
        jedinice = np.where(vr == 1)[0]
        nule = np.where(vr == 0)[0]
        if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1 and s.koefs_problema[i] == 0:
            bazisne_kol += 1

    if bazisne_kol == s.br_vrsta:
        return True
    else:
        return False


# Funkcija za proveru celobrojnosti resenja x1,x2...
def bazisne_celobrojne(s3):

    sve_jed = np.zeros(s3.baz_prom)
    for t in range(s3.baz_prom):

        jedinice = np.where(s3.matricaA[:, t] == 1)[0]
        nule = np.where(s3.matricaA[:, t] == 0)[0]
        if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:
            sve_jed[t] = jedinice

    for i in sve_jed:
        if np.round(s3.matricaB[int(i)], 5) % 1 != 0:
            return False

    return True


def gomorijev_rez(s3):

    ostaci = np.zeros(s3.br_kolona)
    ostatak_rez = 0

    #Ako rezultat fje nije ceo broj racunamo decimalne delove
    if np.round(s3.rez_funkcije, 10) % 1 != 0:
        for i, vr in enumerate(s3.koefs_problema):
            ostaci[i] = vr - math.floor(vr)
        ostatak_rez = s3.rez_funkcije - math.floor(s3.rez_funkcije)

    # Ako postoje x-evi koji nisu celobrojni,
    # uzimamo prvu j-nu od tih ciji rezultat ima decimalni deo != 0 pa po toj vrsti pravimo rez
    else:

        sve_jed = np.zeros(s3.baz_prom)
        razlomljeni = np.zeros(s3.baz_prom)
        for t in range(s3.baz_prom):

            jedinice = np.where(s3.matricaA[:, t] == 1)[0]
            nule = np.where(s3.matricaA[:, t] == 0)[0]
            if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:
                razlomljeni[t] = s3.matricaB[jedinice[0]]
                sve_jed[t] = jedinice

        novi_ostaci = [r - math.floor(r) for r in razlomljeni]

        maks_ostatak = -1
        for i in novi_ostaci:
            if i != 0:
                maks_ostatak = i
                break

        indeks = np.where(novi_ostaci == maks_ostatak)[0]
        indeks_maksa = int(sve_jed[indeks][0])

        for j, vr2 in enumerate(s3.matricaA[indeks_maksa]):
            ostaci[j] = vr2 - math.floor(vr2)

        ostatak_rez = np.array([maks_ostatak])

    ostaci = np.append(ostaci, -1)
    for i, vr in enumerate(ostaci):
        if vr != 0:
            ostaci[i] *= -1

    if ostatak_rez != 0:
        ostatak_rez *= -1

    # Dodajemo novu jednacinu u trenutnu simpleks tablicu
    s3.matricaA = np.append(s3.matricaA, np.zeros((s3.br_vrsta, 1)), axis=1)
    s3.matricaA = np.append(s3.matricaA, [ostaci], axis=0)
    s3.matricaB = np.append(s3.matricaB, [ostatak_rez], axis=0)
    s3.koefs_problema = np.append(s3.koefs_problema, 0)
    s3.br_vrsta += 1
    s3.br_kolona += 1

    # Ako je decimalni deo manji od 0.01 zaokruzujemo na ceo broj
    zaokruzi(s3)

    return s3


def dvofazni_simpleks(s, jedn_ili_vece):

    print("\n######################Prva faza:######################\n")
    s2 = Sistem()
    s2 = copy.deepcopy(s)
    s2.koefs_problema = np.zeros((len(s.koefs_problema)))

    print(s2.rez_funkcije)
    s2.rez_funkcije[0] = 0

    # Ako je neko b < 0 mnozimo celu vrstu sa -1
    for p, l in enumerate(s2.matricaB):
        if l[0] < 0:
            s2.matricaA[p][s2.matricaA[p] != 0] *= -1
            s2.matricaB[p][0] *= -1

    for i in range(len(jedn_ili_vece)):
        if jedn_ili_vece[i] == ">=" or jedn_ili_vece[i] == "=":
            dodatni = np.zeros((s.br_vrsta, 1))
            dodatni[i] = 1
            s2.matricaA = np.append(s2.matricaA, dodatni, axis=1)
            s2.br_kolona += 1
            s2.koefs_problema = np.append(s2.koefs_problema, 1)
            s2.P = np.append(s2.P, s2.br_kolona - 1)

    s2.P = np.array(list(map(int, s2.P)))

    vestacke = np.where(s2.koefs_problema == 1)[0]

    ispis(s2)

    # Vrsimo elementarne transformacije kako bi dobili bazisne kolone
    ciscenje_koefs_problema(s2)

    ispis(s2)
    print("Trenutna vrednost funkcije:", s2.rez_funkcije[0])

    print("Pozivamo tablicni simplex u prvoj fazi:")
    tablicni_simpleks(s2)

    if s2.rez_funkcije[0] != 0:
        print("\n Rezultat pomocnog problema:", s2.rez_funkcije[0],
              "!= 0 => pocetni problem nema dopustivih resenja. STOP")
        s2.rez_funkcije[0] = float('-inf')
        return
        #exit()

    # Brisanje vestackih promenljivih
    pom = np.array([])
    for i in vestacke:
        if (len(np.where(s2.matricaA[:, i] == 1)[0]) != 1 or \
                len(np.where(s2.matricaA[:, i] == 0)[0]) != s2.br_vrsta - 1) or s2.koefs_problema[i] != 0:
            s2.matricaA[:, i] = np.zeros(s2.br_vrsta)
            s2.koefs_problema[i] = 0
            pom = np.append(pom, i)
            vestacke = np.delete(vestacke, np.where(vestacke == i))

    # Prolazimo preostale vestacke bazisne kolone i brisemo odgovarajucu vrstu ako su sve nule u vrsti ili
    # nalazimo pivot i obavljamo transformacije
    for i in vestacke:

        jedinice = np.where(s2.matricaA[:, i] == 1)[0]
        nule = np.where(s2.matricaA[:, i] == 0)[0]

        if len(jedinice) == 1 and len(nule) == s2.br_vrsta - 1:

            indeks_vr = jedinice[0]
            ne_nule = np.where(s2.matricaA[indeks_vr, :] != 0)[0]

            # Ako su sve nule u vrsti osim jedinice koja pripada bazisnoj koloni -> brisemo vrstu
            if len(ne_nule) == 1 and ne_nule[0] == i:

                s2.matricaA = np.delete(s2.matricaA, indeks_vr, axis=0)
                s2.br_vrsta -= 1

            # Nasli smo ne nula vrednost u vrsti, uzimamo za pivot i obavljamo elem. transformacije
            else:

                # novi pivot je prvi != 0 u toj vrsti
                if ne_nule[0] != i:  # da ne uzmemo bas tog jedinog keca

                    pivot_vrsta = indeks_vr
                    pivot_kolona = ne_nule[0]
                    pivot_vrednost = s2.matricaA[pivot_vrsta][pivot_kolona]

                    elem_transformacije(s2, pivot_vrsta, pivot_kolona, pivot_vrednost)

    # Brisemo sve vestacke kolone
    pom = np.append(pom, vestacke)
    s2.matricaA = np.delete(s2.matricaA, pom, axis=1)
    s2.koefs_problema = np.delete(s2.koefs_problema, pom, axis=0)
    s2.br_kolona -= len(pom)

    print("\n######################Druga faza:######################\n")

    s3 = copy.deepcopy(s2)
    s3.koefs_problema = s.koefs_problema
    s3.br_kolona = len(s3.matricaA[0])
    s3.br_vrsta = len(s3.matricaA)

    s3.rez_funkcije[0] = s.rez_funkcije[0]

    ciscenje_koefs_problema(s3)

    tablicni_simpleks(s3)
    s = copy.deepcopy(s3)
    return s


def main():
    s = Sistem()
    unesiUlaz(s)
    jedn_ili_vece = np.copy(s.niz_znakova)

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

    # Pozivamo odgovarajuci Simpleks
    if negativni_c(s) and postoji_baza(s):

        print("C ima negativnih pozivamo tablicni simpleks\n")
        tablicni_simpleks(s)

    elif negativni_b(s) and postoji_baza(s):

        print("B ima negatinvih pozivamo dualni simpleks\n")
        dualni_simpleks(s)

    else:   # nema pocetne baze

        print("Nemamo pocetnu bazu pozivamo dvofazni simpleks\n")
        s = dvofazni_simpleks(s, jedn_ili_vece)

    baz_cel = bazisne_celobrojne(s)
    iteracija = 1

    while not baz_cel:

        gomorijev_rez(s)
        print("Gomorijev rez:", iteracija)
        ispis(s)
        dualni_simpleks(s)
        baz_cel = bazisne_celobrojne(s)
        iteracija += 1


if __name__ == '__main__':
    main()
