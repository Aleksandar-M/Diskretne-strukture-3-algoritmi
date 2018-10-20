import numpy as np


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0     # rezultat funkcije!
        self.problem = ""
        self.koefs_problema = np.array([])
        self.niz_znakova = np.array([])
        self.matricaA = np.array([])
        self.matricaB = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])


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
        print("koefs nejednacine i duzina:", koefs_nejednacine, len(koefs_nejednacine))
        duzina = len(koefs_nejednacine)
        for j in range(duzina):
            if j == duzina-1:
                s.matricaB[i][0] = koefs_nejednacine[j]
            else:
                s.matricaA[i][j] = koefs_nejednacine[j]


def kanonskiOblik(s):

    j = s.br_kolona
    print("nova matrica A, j:", s.matricaA, j)

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        #s.problem = "min"
        s.koefs_problema *= (-1)

    for i in range(s.br_kolona):
        s.Q = np.append(s.Q, i)

    # Prebacujemo nejednacine u jednacine, kao i uslov da b>=0
    for i in range(s.br_vrsta):

        if s.niz_znakova[i] != "=":

            nule = np.zeros((s.br_vrsta, 1))

            if s.niz_znakova[i] == ">=":
                nule[i][0] = -1
            elif s.niz_znakova[i] == "<=":
                nule[i][0] = 1

            s.matricaA = np.append(s.matricaA, nule, axis=1)

            if s.matricaB[i][0] < 0:
                s.matricaB[i][0] *= -1

            s.niz_znakova[i] = "="
            s.br_kolona += 1  # izmenjen broj kolona!!
            s.P = np.append(s.P, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    print("Q, P na pocetku:", s.Q, s.P)

    s.koefs_problema = np.append(s.koefs_problema, np.zeros((1, s.br_vrsta)))


def proveriUslov(koefs):

    for i in range(len(koefs)):
        if koefs[i] < 0:
            return False

    return True


def pronadjiIndeks(koefs, s):

    for i in range(len(koefs)):
        if koefs[i] < 0:
            return s.Q[i]


def main():

    s = Sistem()

    unesiUlaz(s)
    print(s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          s.matricaA,
          s.matricaB
          )

    kanonskiOblik(s)
    print(s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          s.matricaA,
          s.matricaB,
          s.P,
          s.Q
          )

    print(type(s.P))

    # if s.problem == "max":
    #     s.x = np.array(list(map(int, np.append(np.zeros((1, s.br_vrsta+1)), s.matricaB))))  # obrisano s.br_vrsta +1
    # else:
    s.x = np.array(list(map(int, np.append(np.zeros((1, s.br_kolona - len(s.P))), s.matricaB))))
    print("s.x:", s.x)

    tmp = 0
    while tmp < 100:

        matB = s.matricaA[:, s.P]
        koefsB_u_f = s.koefs_problema[s.P]
        koefsN_u_f = s.koefs_problema[s.Q]
        matN = s.matricaA[:, s.Q]
        print("matB, rezB, matN", matB, s.koefs_problema[s.P], matN)

        u_rez = np.linalg.solve(matB.transpose(), koefsB_u_f)
        print(u_rez)

        CN_prim = koefsN_u_f - np.dot(u_rez, matN)
        print("novi koefs", CN_prim, type(CN_prim))

        if proveriUslov(CN_prim):
            print("KRAJ")
            print("x opt:", s.x)
            print("Konacno f", np.sum(s.koefs_problema * s.x))
            exit()

        j = pronadjiIndeks(CN_prim, s)
        print("j je:", j)

        print(matB, s.matricaA[:, [j]])
        y_rez = np.linalg.solve(matB, s.matricaA[:, [j]])
        print("y_rez:", y_rez)

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
                    print("vrednosti, s.x[i], y_rez[pom]", vrednosti, s.x[i], y_rez[pom])

                pom += 1

            t_kapa = vrednosti.min()
            print("t_kapa:", t_kapa)

            x_pom = np.zeros(len(s.x))
            pom = 0
            print("x pom i s x:", x_pom, s.x)
            for i in range(len(s.x)):
                if i == j:
                    x_pom[i] = t_kapa
                elif i in s.P:
                    print("usao:", i, pom)
                    x_pom[i] = s.x[i] - t_kapa*y_rez[pom]
                    pom += 1
                elif i in s.Q:
                    x_pom[i] = 0

            print("x pom:", x_pom)
            s.x = x_pom

            l = 42  #paziii
            for i in s.P:
                if s.x[i] == 0:
                    l = i

            print("l", l)

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

            staroP = s.P

            s.P = np.delete(s.P, indeksl)
            s.P = np.sort(np.append(s.P, s.Q[indeksj]))
            s.Q = np.delete(s.Q, indeksj)
            s.Q = np.sort(np.append(s.Q, staroP[indeksl]))
            print("novo P, Q", s.P, s.Q)

            tmp += 1


if __name__ == '__main__':
   main()
