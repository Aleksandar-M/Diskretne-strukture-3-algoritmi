import numpy as np
from collections import defaultdict
import sys

class Graf:

    def __init__(self, br_cvorova):
        self.V = br_cvorova
        self.graf = defaultdict(list)

    def dodaj_granu(self, u, v):
        self.graf[u].append(v)
        self.graf[v].append(u)

    def DFS_pom(self, c, posecen):

        posecen[c] = True
        print(c, end=" ")

        for i in self.graf[c]:
            if not posecen[i]:
                self.DFS_pom(i, posecen)

    def DFS_neorj(self, c):

        posecen = [False] * len(self.graf)
        self.DFS_pom(c, posecen)

    def BFS_neorj(self, c):

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

    def prebroj(self, c, posecen):

        posecen[c] = True
        brojac = 1

        for i in self.graf[c]:
            if not posecen[i]:
                brojac = brojac + self.prebroj(i, posecen)

        return brojac

    def obrisi_granu(self, u, v):

        for ind, vr in enumerate(self.graf[u]):
            if vr == v:
                self.graf[u].pop(ind)

        for ind, vr in enumerate(self.graf[v]):
            if vr == u:
                self.graf[v].pop(ind)

    def validna_grana(self, u, v):

        if len(self.graf[u]) == 1:
            return True
        else:

            posecen = [False] * int(self.V)
            br1 = self.prebroj(u, posecen)

            self.obrisi_granu(u, v)

            posecen = [False] * int(self.V)
            br2 = self.prebroj(u, posecen)

            self.dodaj_granu(u, v)

            if br1 > br2:
                return False
            else:
                return True

    def ispisi_od_u(self, u):

        for v in self.graf[u]:
            if self.validna_grana(u, v):
                print(u, "-", v)
                self.obrisi_granu(u, v)
                self.ispisi_od_u(v)

    def ispisi_ojlerov_put(self):

        br_neparnih = 0
        for c in range(int(self.V)):
            if len(self.graf[c]) % 2 != 0:
                br_neparnih += 1

        if br_neparnih > 2 or br_neparnih == 1:
            print("Ne postoji Ojlerov put/cikl, broj neparnih cvorova:", br_neparnih)
            exit()

        u = 0
        for i in range(int(self.V)):
            if len(self.graf[i]) % 2 != 0:
                u = i
                break
        self.ispisi_od_u(u)


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
    print("\n############# BFS #############")
    g.BFS_neorj(start)
    print("############# DFS #############")
    g.DFS_neorj(start)
    print("\n############# Fleury-ev algoritam #############")
    g.ispisi_ojlerov_put()


if __name__ == '__main__':
    main()
