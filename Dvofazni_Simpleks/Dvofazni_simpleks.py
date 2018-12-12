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

        # Zaokruzivanje mnogo malih brojva blizu nule na 0
        s2.matricaA[abs(s2.matricaA) < 0.00001] = 0
        s2.matricaB[abs(s2.matricaB) < 0.00001] = 0
        s2.koefs_problema[abs(s2.koefs_problema) < 0.00001] = 0
        s2.rez_funkcije[abs(s2.rez_funkcije) < 0.00001] = 0

    # Delimo celu vrstu sa trenutnim pivotom
    if pivot_vrednost != 0:
        s2.matricaA[pivot_vrsta] = s2.matricaA[pivot_vrsta] / pivot_vrednost
        s2.matricaB[pivot_vrsta] = s2.matricaB[pivot_vrsta] / pivot_vrednost

        s2.matricaA[abs(s2.matricaA) < 0.00001] = 0
        s2.matricaB[abs(s2.matricaB) < 0.00001] = 0


# Pomocna funkcija za transformisanje koeficijenata ispod bazisnih kolona
def ciscenje_koefs_problema(s3):

    for i in range(s3.br_kolona):

        jedinice = np.where(s3.matricaA[:, i] == 1)[0]
        nule = np.where(s3.matricaA[:, i] == 0)[0]

        if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:

            stari_koef = s3.koefs_problema[i]
            if stari_koef != 0:
                indeks_1 = jedinice[0]
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
                pivot_vrsta = 50
                pivot_kolona = 50
                pivot_vrednost = 50
                for i in range(s.br_vrsta):
                    if s.matricaA[i][k] > 0:
                        nova_vr = s.matricaB[i][0] / s.matricaA[i][k]

                        # Trenutni min
                        if blend == "da":
                            if min > nova_vr:     # Koriscenjem Blendovog pravila
                                min = nova_vr
                                pivot_vrsta = i
                                pivot_kolona = k
                                pivot_vrednost = s.matricaA[i][k]
                        else:
                            if min >= nova_vr:     # Bez koriscenja pravila
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
            
            if s.problem == "min":
                print("min f:", s.rez_funkcije[0]*(-1))
            else:
                print("max f:", s.rez_funkcije[0])

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.2f}'.format(opt_resenje[i]), end=" ")
            print("")
            return

        iteracija += 1


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

    kanonskiOblik(s)
    print("U kanonskom obliku:\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.niz_znakova)
    ispis(s)

    sl_dvofaznog = 1                #######
    if sl_dvofaznog:

        print("\n######################Prva faza:######################\n")
        s2 = Sistem()
        s2 = copy.deepcopy(s)
        s2.koefs_problema = np.zeros((len(s.koefs_problema)))

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
                s2.P = np.append(s2.P, s2.br_kolona-1)

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
            print("\n Rezultat pomocnog problema:", s2.rez_funkcije[0] ,"!= 0 => pocetni problem nema dopustivih resenja. STOP")
            exit()

        # Brisanje vestackih promenljivih
        pom = np.array([])
        for i in vestacke:
            if len(np.where(s2.matricaA[:, i] == 1)[0]) != 1 or \
                    len(np.where(s2.matricaA[:, i] == 0)[0]) != s2.br_vrsta - 1:

                s2.matricaA[:, i] = np.zeros(s2.br_vrsta)
                s2.koefs_problema[i] = 0
                pom = np.append(pom, i)
                vestacke = np.delete(vestacke, np.where(vestacke == i))

        # Prolazimo preostale vestacke bazisne kolone i brisemo odgovarajucu vrstu ako su sve nule u vrsti ili
        # nalazimo pivot i obavljamo transformacije
        for i in vestacke:

            jedinice = np.where(s2.matricaA[:, i] == 1)[0]
            nule = np.where(s2.matricaA[:, i] == 0)[0]

            if len(jedinice) == 1 and len(nule) == s2.br_vrsta-1:

                indeks_vr = jedinice[0]
                ne_nule = np.where(s2.matricaA[indeks_vr, :] != 0)[0]

                # Ako su sve nule u vrsti osim jedinice koja pripada bazisnoj koloni -> brisemo vrstu
                if len(ne_nule) == 1 and ne_nule[0] == i:

                    s2.matricaA = np.delete(s2.matricaA, indeks_vr, axis=0)
                    s2.br_vrsta -= 1

                # Nasli smo ne nula vrednost u vrsti, uzimamo za pivot i obavljamo elem. transformacije
                else:

                    #novi pivot je prvi != 0 u toj vrsti
                    if ne_nule[0] != i:                     # da ne uzmemo bas tog jedinog keca

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

        ciscenje_koefs_problema(s3)

        tablicni_simpleks(s3)
        exit()

    else:
        tablicni_simpleks(s)
    exit()


if __name__ == '__main__':
    main()
