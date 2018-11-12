import numpy as np
import math

np.set_printoptions(suppress=True, precision=3)


class Sistem:

    def __init__(self):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0
        self.problem = ""
        self.koefs_problema = np.array([])
        self.matricaA = np.array([])
        self.b = 0
        self.x = np.array([0])
        self.k_y = np.zeros((1, 1))
        self.i_y = np.zeros((1, 1))
        self.resenje = np.array([])
        self.global_rez = np.array([[-1,-1,-1,-1]])
        self.dubina = np.array([])


metod = 2

# Funkcija za unos
def unesiUlaz(s):

    global metod

    funkcija = input("Unesite problem u obliku max i koeficijente funkcije:").split(" ")

    if funkcija[0] == "max":
        s.problem = str(funkcija[0])
    else:
        print("\n Pogresan unos problema.")
        exit()

    s.koefs_problema = np.array(list(map(float, funkcija[1:])))

    linija = input("Unesite sve koeficijente nejednacine kao i znak:").split(" ")
    koefs_nejednacine = list(map(float, linija[:-2] + linija[-1:]))

    s.b = int(koefs_nejednacine[-1])
    s.matricaA = np.array(koefs_nejednacine[:-1])

    pocetni_xevi = input("Unesite pocetne xeve:")
    if pocetni_xevi != "":
        s.x = list(map(int, pocetni_xevi.split(" ")))
    print(s.x)

    metod = int(input("Unesite 1 ili 2 za metod:"))
    print(metod, type(metod))

def nadji_optimalno(niz, dubina, s, k, opt):

    if k == 0:  # ili 1
        print("Optimalno:", opt)
        return
    else:
        ind1 = np.where(niz == max(niz))[0]
        opt = np.append(opt, ind1)   # dodajemo u optimalno
        print(s.global_rez, niz)
        ind3 = np.where(np.prod(s.global_rez == niz, axis=-1))[0]
        ind2 = np.where(dubina == k)[0]
        print("indeksi", ind1, ind2, ind3)

        for t in s.global_rez:

            tmp = np.where(t == max(niz))[0]
            if len(tmp) != 0:
                print(np.where(np.prod(s.global_rez == t, axis=-1))[0])


        exit()




def metod_unazad(k, s, vr):

    print("metod k vr", k, vr)
    rez1 = np.array([])
    if k == 1:

        print("kad k==1", s.koefs_problema[0], math.floor(vr/s.matricaA[0]))
        return s.koefs_problema[0] * math.floor(vr/s.matricaA[0])

    else:

        rez = np.array([])
        if math.floor(vr/s.matricaA[k-1]) not in s.x:
            s.x = np.append(s.x, math.floor(vr/s.matricaA[k-1]))   # gledmao indekse kao 1...
            print("s.x", s.x)

        for i in s.x:
            if vr - s.matricaA[k-1]*i >= 0:

                print("for s.b, s.matricaA[k-1], i", vr, s.matricaA[k - 1], i)
                rez = np.append(rez, s.koefs_problema[k-1]*i + metod_unazad(k-1, s, vr - s.matricaA[k-1]*i))
                print("IZLAZ NAKON I-TOG", k, i)

        print("rez:", rez)
        print("===================max od rez", max(rez))
        print("indeks za x:::::::::::", np.where(rez == max(rez))[0])

        if len(rez) < 4:
            l = 4 - len(rez)
            tmp = np.repeat(-1, l)
            rez = np.append(rez, tmp)

        s.global_rez = np.append(s.global_rez, [rez], axis=0)
        s.dubina = np.append(s.dubina, k-1)
        # print("global rez\n", s.global_rez)
        # print("dubina", s.dubina)
        return max(rez)


def metod_i(k, vr, rez, s, levo):

    if k == 1:
        if rez == 0:
            s.i_y[1][int(vr)] = 0
        else:
            s.i_y[1][int(vr)] = 1

    elif k > 1:
        if rez == levo:
            print("USAOOO U REZ JEDN LEVO", s.i_y[k-1][int(vr)], k)
            s.i_y[k][int(vr)] = s.i_y[k-1][int(vr)]
        else:
            s.i_y[k][int(vr)] = k


def metod_unapred(k, s, vr):

    for i in range(k):
        print(i)
        for j in range(int(s.b)+1):
            if i == 0:
                continue
            elif i == 1:
                print("...", s.koefs_problema[i-1], math.floor(j/s.matricaA[i-1]))
                s.k_y[i][j] = s.koefs_problema[i-1] * math.floor(j/s.matricaA[i-1])

                print("metod i", i, j, s.k_y[i][j])
                metod_i(i, j, s.k_y[i][j], s, 0)

            else:
                if j-s.matricaA[i-1] < 0:
                    s.k_y[i][j] = max(s.k_y[i-1][j], -50)
                    metod_i(i, j, s.k_y[i][j], s, s.k_y[i - 1][j])
                else:
                    s.k_y[i][j] = max(s.k_y[i-1][j], s.koefs_problema[i-1] + s.k_y[i-1][int(j-s.matricaA[i-1])])
                    metod_i(i, j, s.k_y[i][j], s, s.k_y[i - 1][j])


def pronadji_resenje(s):

    s.resenje = np.zeros(len(s.koefs_problema))
    b = s.b

    while b > 0:

        pom = s.i_y[-1][int(b)]
        s.resenje[int(pom)-1] += 1
        b -= s.matricaA[int(pom)-1]


def main():

    s = Sistem()

    unesiUlaz(s)
    print(s.problem, s.koefs_problema, s.matricaA, s.b)

    # Problem unapred
    if metod == 2:

        s.k_y = np.zeros((len(np.where(s.matricaA != 0)[0])+1, s.b+1))
        s.i_y = np.zeros((len(np.where(s.matricaA != 0)[0])+1, s.b+1))
        metod_unapred(len(np.where(s.matricaA != 0)[0])+1, s, s.b)

        print("krajnje s.ky\n", s.k_y)
        print("krajnje s.iy\n", s.i_y)
        pronadji_resenje(s)
        print("F max:", s.k_y[-1][-1])
        print("Za x:", s.resenje)

    # Problem unazad
    else:
        opt = np.array([])
        metod_unazad(len(s.matricaA), s, s.b)
        s.global_rez = s.global_rez[1:]  # skinuli prvi bespotrebni red
        # nadji_optimalno(s.global_rez[-1], s.dubina, s,
        #                 len(s.koefs_problema) - 1, opt)


if __name__ == '__main__':
    main()