import numpy as np
import copy

np.set_printoptions(suppress=True, precision=2)

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
        s.problem = "min"
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


# Pomocna funkcija za lep ispis matrice
def ispisiMatricu(mat):
    for vrsta in mat:
        for kolona in vrsta:
            if kolona >= 0:
                print(" ", round(kolona), sep="", end=" ")
            else:
                print(round(kolona), end=" ")
        print("")
    print("")


def simplex(s):
    s.x = np.array(list(map(int, np.append(np.zeros((1, s.br_kolona - len(s.P))), s.matricaB))))
    print("Pocetno resenje:", s.x)

    matB = s.matricaA[:, s.P]

    # for i in range(s.br_kolona):
    #     if sum(s.matricaA[:, i]) == 1:
    #         print("JESAM JEDNAK KECU, indeks i, nizP", i, s.P)
    #         print(s.matricaA[:, i])
    #
    #         if s.koefs_problema[i] != 0:
    #
    #             for t in range(s.br_vrsta):
    #                 if s.matricaA[t][i] == 1:
    #                     indeks_1 = t
    #
    #             s.koefs_problema = s.koefs_problema + (-1)*s.koefs_problema[i]*s.matricaA[indeks_1, :]
    #             print("----", s.rez_funkcije, (-1)*s.koefs_problema[i], s.matricaB[indeks_1, :])
    #             s.rez_funkcije = s.rez_funkcije + (-1)*s.matricaB[indeks_1, :]
    #
    # print("pblabla ::\n", s.br_vrsta,
    #       s.br_kolona,
    #       s.rez_funkcije,
    #       s.problem,
    #       s.koefs_problema,
    #       s.niz_znakova,
    #       s.matricaA,
    #       s.matricaB,
    #       s.P,
    #       s.Q,
    #       s.x)


    iteracija = 1
    while iteracija < 100:

        print("Iteracija :", iteracija)

        matN = s.matricaA[:, s.Q]
        koefsB_u_f = s.koefs_problema[s.P]
        koefsN_u_f = s.koefs_problema[s.Q]
        print("matB:")
        ispisiMatricu(matB)
        print("matN:")
        ispisiMatricu(matN)

        u_rez = np.linalg.solve(matB.transpose(), koefsB_u_f)
        print("Resenje sistema za u:\n", u_rez)

        CN_prim = koefsN_u_f - np.dot(u_rez, matN)
        print("Novi koeficijenti:\n", CN_prim)

        # Ako su svi koeficijenti pozitivni, nasli smo optimalno resenje
        if proveriUslov(CN_prim):
            print("\nx optimalno:", s.x)
            print("Konacno f:", np.sum(s.koefs_problema * s.x))
            #exit()

            print("pre returna ::\n", s.br_vrsta,
                  s.br_kolona,
                  s.rez_funkcije,
                  s.problem,
                  s.koefs_problema,
                  s.niz_znakova,
                  s.matricaA,
                  s.matricaB,
                  s.P,
                  s.Q,
                  s.x)

            return 1


        j = pronadjiIndeks(CN_prim, s)
        print("j je:", j)

        y_rez = np.linalg.solve(matB, s.matricaA[:, [j]])
        print("Resenje sistema za y:")
        ispisiMatricu(y_rez)

        # Provera ako je problem neogranicen
        br_neg = 0
        for i in range(len(y_rez)):
            if y_rez[i] <= 0:
                br_neg += 1

        if br_neg == len(y_rez):

            print("STOP: Problem je neogranicen")
            exit()

        else:

            vrednosti = np.array([])
            pom = 0

            for i in s.P:

                if y_rez[pom] > 0:
                    vrednosti = np.append(vrednosti, s.x[i] / y_rez[pom])

                pom += 1

            t_kapa = vrednosti.min()
            print("t kapa:", t_kapa)

            x_novo = np.zeros(len(s.x))
            pom = 0

            for i in range(len(s.x)):
                if i == j:
                    x_novo[i] = t_kapa

                elif i in s.P:

                    p = 42
                    for d in range(len(s.P)):
                        if i == s.P[d]:
                            p = d

                    x_novo[i] = s.x[i] - t_kapa * y_rez[p]
                    pom += 1

                elif i in s.Q:
                    x_novo[i] = 0

            print("x novo:", x_novo)
            s.x = x_novo

            l = 42
            for i in s.P:
                if s.x[i] == 0:
                    l = i

            print("l je:", l)

            indeksl = 42
            indeksj = 42
            for i in range(len(s.P)):
                if s.P[i] == l:
                    indeksl = i

            for i in range(len(s.Q)):
                if s.Q[i] == j:
                    indeksj = i

            if indeksj == 42 or indeksl == 42:
                print("Greska, nije pronadjen neki od indeksa za j, l")
                exit()

            # Pravimo novo P, Q
            staroP = np.copy(s.P)
            s.P[indeksl] = s.Q[indeksj]
            s.Q[indeksj] = staroP[indeksl]
            print("Novo P, Q:", s.P + 1, s.Q + 1)

            # Pravimo eta matricu
            matE = np.identity(len(s.P))
            novaKolona = y_rez
            leviKraj = matE[:, :indeksl]
            desniKraj = matE[:, indeksl + 1:]
            leviKraj = np.append(leviKraj, novaKolona, axis=1)
            leviKraj = np.append(leviKraj, desniKraj, axis=1)
            matE = leviKraj
            print("matrica E:")
            ispisiMatricu(leviKraj)

            # Pravimo novu matricu B kao staro B pomnozeno sa eta matricom
            matB = np.dot(matB, matE)

            iteracija += 1

def tablicni_simpleks(s):

    iteracija = 0
    while iteracija < 100:

        for k in range(len(s.matricaB)):
            if s.matricaB[k] < 0:
                print("skoef", s.matricaB[k], k)

                # Provera da li su svi iznad c negativni ako T -> neogranicen problem
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
                        nova_vr = s.koefs_problema[i] / s.matricaA[k][i]    # koefs_problema[0][i]????

                        # Trenutni max
                        if max < nova_vr:
                            max = nova_vr
                            pivot_vrsta = k
                            pivot_kolona = i
                            pivot_vrednost = s.matricaA[k][i]


                print("pivot vrsta, kolona, vrednost", pivot_vrsta, pivot_kolona, pivot_vrednost)

                for i in range(s.br_vrsta):

                    if i != pivot_vrsta:
                        print("starmo smatA", s.matricaA[i])
                        stara_pivot_kolona = s.matricaA[i][pivot_kolona]
                        print("sdsadas", stara_pivot_kolona)
                        s.matricaA[i] = s.matricaA[i] + (-1)*stara_pivot_kolona/pivot_vrednost*s.matricaA[pivot_vrsta]
                        print("s.m..", s.matricaA[i], (-1)*stara_pivot_kolona,pivot_vrednost)
                        s.matricaB[i] = s.matricaB[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaB[pivot_vrsta]

                    stara_pivot_kolona_c = s.koefs_problema[pivot_kolona]
                    s.koefs_problema = s.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaA[pivot_vrsta]
                    s.rez_funkcije = s.rez_funkcije + (-1)*stara_pivot_kolona_c/pivot_vrednost * s.matricaB[pivot_vrsta]


                    print("pblabla ::\n", s.br_vrsta,
                          s.br_kolona,
                          s.rez_funkcije,
                          s.problem,
                          s.koefs_problema,
                          s.niz_znakova,
                          s.matricaA,
                          s.matricaB,
                          s.P,
                          s.Q,
                          s.x)

                # Delimo celu vrstu sa trenutnim pivotom
                if pivot_vrednost != 0:
                    print("usao u sredjivanjeeee")
                    s.matricaA[pivot_vrsta] = s.matricaA[pivot_vrsta] / pivot_vrednost
                    s.matricaB[pivot_vrsta] = s.matricaB[pivot_vrsta] / pivot_vrednost

        br_pozitivnih = 0
        for i in range(len(s.matricaB)):
            if s.matricaB[i] >= 0:
                br_pozitivnih += 1

        if br_pozitivnih == len(s.matricaB):
            print("Kraj ::\n", s.br_vrsta,
                  s.br_kolona,
                  s.rez_funkcije,
                  s.problem,
                  s.koefs_problema,
                  s.niz_znakova,
                  "\n", s.matricaA,
                  "\n", s.matricaB,"\n",
                  s.P,
                  s.Q,
                  s.x)

            # pronalazenje optimalnog resenja                   #  TREBA PREPRAVITI
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):
                jedinica = np.where(s.matricaA[:, i] == 1)[0]

                if len(jedinica) == 1:
                    opt_resenje[i] = s.matricaB[jedinica[0]]

            print("Optimalno resenje:\n", opt_resenje)
            exit()


def main():

    s = Sistem()

    unesiUlaz(s)

    jedn_ili_vece = np.copy(s.niz_znakova)


    print("jedn ili vece:", jedn_ili_vece)
    print("sve::\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          s.matricaA,
          s.matricaB,
          s.P,
          s.Q,
          s.x)

    # Ako je bila nejednacina oblika >= hocemo <=
    for i in range(s.br_vrsta):
        if s.niz_znakova[i] == ">=":
            s.matricaB[i] *= -1
            s.matricaA[i] *= -1
            s.niz_znakova[i] = "<="

    kanonskiOblik(s)
    print("sve kanonski::\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          s.matricaA,
          s.matricaB,
          s.P,
          s.Q,
          s.x)
    print("\n\nQ, P na pocetku:", s.Q + 1, s.P + 1)


    print("pomnozeno pre simpleksa::\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          s.matricaA,
          s.matricaB,
          s.P,
          s.Q,
          s.x)
    tablicni_simpleks(s)




if __name__ == '__main__':
    main()
