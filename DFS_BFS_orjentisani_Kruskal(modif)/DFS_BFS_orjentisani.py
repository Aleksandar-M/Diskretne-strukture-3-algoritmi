from collections import defaultdict
import sys


class Graf:

    def __init__(self, br_cvorova):
        self.V = br_cvorova
        self.graf = defaultdict(list)

    def dodaj_granu(self, u, v):
        self.graf[u].append(v)

    def sve_obradjene(self, v, direkt, napred, obrat, presek):

        for t in self.graf[v]:

            grana = (v, t)
            if grana not in direkt + napred + obrat + presek:
                return False, grana

        return True, 1

    def DFS_orj(self, start):

        direkt = []
        napred = []
        obrat = []
        presek = []
        tren_dub = 1

        indeks = [0] * int(self.V)
        otac = [None] * int(self.V)
        obrada = [0] * int(self.V)
        dubina = [0] * int(self.V)

        # Krecemo od start cvora pretragu
        dubina[start] = tren_dub
        indeks[start] = 1
        v = start

        while 1:

            while not self.sve_obradjene(v, direkt, napred, obrat, presek)[0]:

                v, w = self.sve_obradjene(v, direkt, napred, obrat, presek)[1]
                if indeks[w] == 0:

                    tren_dub += 1
                    dubina[w] = tren_dub
                    direkt.append((v, w))
                    indeks[w] = 1
                    otac[w] = v
                    v = w

                else:

                    if dubina[w] > dubina[v]:
                        napred.append((v, w))
                    elif dubina[w] < dubina[v]:
                        if obrada[w] == 0:
                            obrat.append((v, w))
                        else:
                            presek.append((v, w))

            obrada[v] = 1
            if otac[v] is not None:
                v = otac[v]
            else:
                print("Grane koje grade razapinjucu sumu:\n", direkt)
                return direkt

    def BFS_orj(self, c):

        Q = []
        posecen = [0] * len(self.graf)
        p = ['-'] * len(self.graf)
        l = ['-'] * len(self.graf)
        t = ['-'] * len(self.graf)

        Q.append(c)
        posecen[c] = 1
        l[c] = 0
        t[c] = 1
        ispis(Q, posecen, p, l, t)

        while Q:

            c = Q[0]

            for i in self.graf[c]:
                if posecen[i] == 0:
                    Q.append(i)
                    posecen[i] = 1
                    p[i] = c
                    l[i] = l[c] + 1
                    t[i] = sum(posecen)

                    ispis(Q, posecen, p, l, t)

            if sum(posecen) == len(self.graf):

                while Q:
                    ispis(Q, posecen, p, l, t)
                    Q.pop(0)
            else:
                Q.pop(0)


def ispis(Q, posecen, p, l, t):

    sp = " "
    br1 = 0
    br2 = 0

    for i in p:
        if i != '-':
            br1 += 1

    for i in l:
        if i != '-':
            br2 += 1

    if len(p) < 10:
        print(Q, sp*3*(len(posecen)-len(Q)), posecen, sp, p, br1*2*sp, l, br1*2*sp, t)
    else:
        print(Q, "\n", posecen, "\n", p, "\n", l, "\n", t)
        print("----------")


def unesi_graf():

    V = input("Unesi broj cvorova:")
    graf = Graf(V)

    for linija in sys.stdin:

        linija = linija.strip().split(" ")
        graf.dodaj_granu(int(linija[0]), int(linija[1]))

    return graf


def main():

    start = 0
    g = unesi_graf()
    print(g.graf)
    print("############# DFS #############")
    g.DFS_orj(start)
    print("############# BFS #############")
    g.BFS_orj(start)


if __name__ == '__main__':
    main()