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
            if j == duzina-1:
                s.matricaB[i][0] = koefs_nejednacine[j]
            else:
                s.matricaA[i][j] = koefs_nejednacine[j]


# Funkcija za svodjenje na kanonski oblik
def kanonskiOblik(s):

    j = s.br_kolona

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        s.problem = "min"
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
            s.br_kolona += 1         # Izmenjen broj kolona
            s.P = np.append(s.P, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    s.koefs_problema = np.append(s.koefs_problema, np.zeros((1, len(s.P))))


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


def main():

    s = Sistem()

    unesiUlaz(s)
    kanonskiOblik(s)
    print("\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.koefs_problema,
          s.niz_znakova,
          "\n", s.matricaA,
          "\n", s.matricaB,
          "\n Q, P na pocetku:", s.Q, s.P
          )

    s.x = np.array(list(map(int, np.append(np.zeros((1, s.br_kolona - len(s.P))), s.matricaB))))
    print("Pocetno resenje:", s.x)

    iteracija = 1
    while iteracija < 100:

        print("Iteracija :", iteracija)
        matB = s.matricaA[:, s.P]
        matN = s.matricaA[:, s.Q]
        koefsB_u_f = s.koefs_problema[s.P]
        koefsN_u_f = s.koefs_problema[s.Q]
        print("matB, matN: \n", matB, "\n", matN)

        u_rez = np.linalg.solve(matB.transpose(), koefsB_u_f)
        print("Resenje sistema za u:\n", u_rez)

        CN_prim = koefsN_u_f - np.dot(u_rez, matN)
        print("Novi koeficijenti:\n", CN_prim)

        # Ako su svi koeficijenti pozitivni, nasli smo optimalno resenje
        if proveriUslov(CN_prim):
            print("\nx optimalno:", s.x)
            print("Konacno f:", np.sum(s.koefs_problema * s.x))
            exit()

        j = pronadjiIndeks(CN_prim, s)
        print("j je:", j)

        #print(matB, "\n", s.matricaA[:, [j]])
        y_rez = np.linalg.solve(matB, s.matricaA[:, [j]])
        print("Resenje sistema za y:\n", y_rez)

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

                    x_novo[i] = s.x[i] - t_kapa*y_rez[pom]
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
            staroP = s.P
            s.P = np.delete(s.P, indeksl)
            s.P = np.sort(np.append(s.P, s.Q[indeksj]))
            s.Q = np.delete(s.Q, indeksj)
            s.Q = np.sort(np.append(s.Q, staroP[indeksl]))
            print("Novo P, Q", s.P, s.Q)

            iteracija += 1


if __name__ == '__main__':
   main()
