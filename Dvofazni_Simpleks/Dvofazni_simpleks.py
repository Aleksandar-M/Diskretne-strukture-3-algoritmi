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
        print("ITERACIJAA", iteracija)
        for k in range(len(s.koefs_problema)):
            print("k koeficijenti problema", k, s.koefs_problema)

            if s.koefs_problema[k] < 0:
                print("skoef", s.koefs_problema[k], k)

                # Provera da li su svi iznad c negativni ako T -> neogranicen problem
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
                        if min > nova_vr:
                            min = nova_vr
                            pivot_vrsta = i
                            pivot_kolona = k
                            pivot_vrednost = s.matricaA[i][k]


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
                    s.matricaA[pivot_vrsta] = s.matricaA[pivot_vrsta] / pivot_vrednost
                    s.matricaB[pivot_vrsta] = s.matricaB[pivot_vrsta] / pivot_vrednost

        br_pozitivnih = 0
        for i in range(len(s.koefs_problema)):
            if s.koefs_problema[i] >= 0:
                br_pozitivnih += 1

        if br_pozitivnih == len(s.koefs_problema):
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
            if s.problem == "min":
                print("min f:", s.rez_funkcije[0]*(-1))
            else:
                print("max f:", s.rez_funkcije[0])
            # pronalazenje optimalnog resenja
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):
                jedinica = np.where(s.matricaA[:, i] == 1)[0]

                if len(jedinica) == 1:
                    opt_resenje[i] = s.matricaB[jedinica[0]]

            print("Optimalno resenje:\n", opt_resenje)
            return

        iteracija += 1


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

    sl_dvofaznog = 1                # RUCNO PROMENI DA RADI DVOFAZNI---
    if sl_dvofaznog:
        print("prvi test dvofaznog")
        s2 = Sistem()
        s2 = copy.deepcopy(s)
        s2.koefs_problema = np.zeros((len(s.koefs_problema)))
        print("sada s2", s2.niz_znakova)
        print("Pravimo pomocni problem:")

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
        print("vestacke:", vestacke)

        print("nova matrica A i sve za s2::\n", s2.br_vrsta,
              s2.br_kolona,
              s2.rez_funkcije,
              s2.problem,
              s2.koefs_problema,
              s2.niz_znakova,
              s2.matricaA,
              s2.matricaB,
              s2.P,
              s2.Q,
              s2.x)

        for i in range(s2.br_kolona):
            if len(np.where(s2.matricaA[:, i] == 1)[0]) == 1:  #!= 0:
                print("jednak 1, indeks i, nizP", i, s2.P)
                print(s2.matricaA[:, i])

                if s2.koefs_problema[i] != 0:

                    for t in range(s2.br_vrsta):
                        if s2.matricaA[t][i] == 1:
                            indeks_1 = t

                    s2.koefs_problema = s2.koefs_problema + (-1)*s2.koefs_problema[i]*s2.matricaA[indeks_1, :]
                    print("----", s2.rez_funkcije, (-1)*s2.koefs_problema[i], s2.matricaB[indeks_1, :])
                    s2.rez_funkcije = s2.rez_funkcije + (-1)*s2.matricaB[indeks_1, :]

        print("Izlaz nakon anuliranja ispod jedinicne kolone::\n", s2.br_vrsta,
              s2.br_kolona,
              s2.rez_funkcije,
              s2.problem,
              s2.koefs_problema,
              s2.niz_znakova,
              s2.matricaA,
              s2.matricaB,
              s2.P,
              s2.Q,
              s2.x)

        print("Pozivamo tablicni simplex u prvoj fazi:")
        tablicni_simpleks(s2)

        # Brisanje vestackih promenljivih                       ZAHTEVA PREPRAVKU!!!!!!!!!!!!!!!!!
        pom = np.array([])
        for i in vestacke:
            if len(np.where(s2.matricaA[:, i] == 1)[0]) != 1 or \
                    len(np.where(s2.matricaA[:, i] == 0)[0]) != s2.br_vrsta - 1:

                s2.matricaA[:, i] = np.zeros(s2.br_vrsta)
                s2.koefs_problema[i] = 0
                pom = np.append(pom, i)
                vestacke = np.delete(vestacke, np.where(vestacke == i))

        print("nakon prvog dela NE brisanja pom vesstacke:", s2.matricaA, s2.koefs_problema, s2.br_kolona, pom, vestacke)

        for i in vestacke:
            print("i i broj kolona", i, vestacke)
            print("ima keceva u koloni:", np.where(s2.matricaA[:, i] == 1)[0])
            print("ima nula u koloni:", np.where(s2.matricaA[:, i] == 0)[0])


            if len(np.where(s2.matricaA[:, i] == 1)[0]) == 1 and \
                    len(np.where(s2.matricaA[:, i] == 0)[0]) == s2.br_vrsta-1:
                print("indeks_vr (porveriti):", np.where(s2.matricaA[:, i] == 1)[0][0])
                indeks_vr = np.where(s2.matricaA[:, i] == 1)[0][0]

                ne_nule = np.where(s2.matricaA[indeks_vr, :] != 0)[0]
                print("ne nule u vrsti", ne_nule)

                if len(ne_nule) == 1 and ne_nule[0] == i:
                    print("brisem govno", s2.matricaA, i)
                    s2.matricaA = np.delete(s2.matricaA, indeks_vr, axis=0)
                    s2.br_vrsta -= 1
                    #pom = np.append(pom, i)


                else:
                    #novi pivot je prvi != 0 u toj vrsti
                    #po njemu sad azuriramo matricu
                    if ne_nule[0] != i:                     # da ne uzmemo bas tog jedinog keca
                        pivot_vrsta = indeks_vr
                        pivot_kolona = ne_nule[0]
                        pivot_vrednost = s2.matricaA[pivot_vrsta][pivot_kolona]
                        print("pivotiranje za ne nule: vrsta kolona vrednost:", pivot_vrsta, pivot_kolona, pivot_vrednost)

                        for k in range(s2.br_vrsta):

                            if k != pivot_vrsta:
                                #print("starmo smatA", s.matricaA[i])
                                stara_pivot_kolona = s2.matricaA[k][pivot_kolona]
                                #print("sdsadas", stara_pivot_kolona)
                                s2.matricaA[k] = s2.matricaA[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaA[
                                    pivot_vrsta]
                                #print("s.m..", s.matricaA[i], (-1) * stara_pivot_kolona, pivot_vrednost)
                                s2.matricaB[k] = s2.matricaB[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaB[
                                    pivot_vrsta]

                            stara_pivot_kolona_c = s2.koefs_problema[pivot_kolona]
                            s2.koefs_problema = s2.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaA[
                                pivot_vrsta]
                            s2.rez_funkcije = s2.rez_funkcije + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaB[
                                pivot_vrsta]


                        # Delimo celu vrstu sa trenutnim pivotom - isto kao tamo pre
                        if pivot_vrednost != 0:
                            s2.matricaA[pivot_vrsta] = s2.matricaA[pivot_vrsta] / pivot_vrednost
                            s2.matricaB[pivot_vrsta] = s2.matricaB[pivot_vrsta] / pivot_vrednost

                        print("rez posle slucaja pivotinja nekog novog u vrsti gde je 1::\n", s2.br_vrsta,
                              s2.br_kolona,
                              s2.rez_funkcije,
                              s2.problem,
                              s2.koefs_problema,
                              s2.niz_znakova,
                              s2.matricaA,
                              s2.matricaB,
                              s2.P,
                              s2.Q,
                              s2.x)

        pom = np.append(pom, vestacke)
        print("pom jeeee", pom)
        s2.matricaA = np.delete(s2.matricaA, pom, axis=1)
        s2.koefs_problema = np.delete(s2.koefs_problema, pom, axis=0)
        s2.br_kolona -= len(pom)


        print("vestacke", vestacke)
        print("nakon prvog dela  brisanja vesstacke:", s2.matricaA, s2.koefs_problema, s2.br_kolona, vestacke)


        print("posle sredjivanja::\n", s2.br_vrsta,
              s2.br_kolona,
              s2.rez_funkcije,
              s2.problem,
              s2.koefs_problema,
              s2.niz_znakova,
              s2.matricaA,
              s2.matricaB,
              s2.P,
              s2.Q,
              s2.x)

        if s2.rez_funkcije != 0:
            print("pomocni problem != 0, problem neodluciv")
            exit()

        print("faza 2")

        s3 = copy.deepcopy(s2)
        s3.koefs_problema = s.koefs_problema
        s3.br_kolona = len(s3.matricaA[0])
        s3.br_vrsta = len(s3.matricaA)
        print(s3.br_kolona)

        print("pos::\n", s3.br_vrsta,
              s3.br_kolona,
              s3.rez_funkcije,
              s3.problem,
              s3.koefs_problema,
              s3.niz_znakova,
              s3.matricaA,
              s3.matricaB,
              s3.P,
              s3.Q,
              s3.x)

        for i in range(s3.br_kolona):
            if len(np.where(s3.matricaA[:, i] == 1)[0]) == 1:    # != 0
                print("jednak 1, indeks i, nizP", i, s3.P)
                print(s3.matricaA[:, i])

                if s3.koefs_problema[i] != 0:

                    for t in range(s3.br_vrsta):
                        if s3.matricaA[t][i] == 1:
                            indeks_1 = t

                    stari_koef = s3.koefs_problema[i]
                    print(s3.koefs_problema , s3.koefs_problema[i], s3.matricaA[indeks_1, :])
                    s3.koefs_problema = s3.koefs_problema + (-1)*s3.koefs_problema[i]*s3.matricaA[indeks_1, :]
                    print("sada", s3.koefs_problema)
                    print("----", s3.rez_funkcije, (-1)*s3.koefs_problema[i], s3.matricaB[indeks_1, :])
                    s3.rez_funkcije = s3.rez_funkcije + (-1)*stari_koef*s3.matricaB[indeks_1, :]
                    print("Trenutni rezultat fje:", s3.rez_funkcije)

        print("ulaz za tablicni::\n", s3.br_vrsta,
              s3.br_kolona,
              s3.rez_funkcije,
              s3.problem,
              s3.koefs_problema,
              s3.niz_znakova,
              s3.matricaA,
              s3.matricaB,
              s3.P,
              s3.Q,
              s3.x)

        #simplex(s3)
        tablicni_simpleks(s3)

        exit()

    else:
        tablicni_simpleks(s)
    exit()


if __name__ == '__main__':
    main()
