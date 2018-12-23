import sys


class Graf:

    def __init__(self, br_cvorova):
        self.V = br_cvorova
        self.grane = []
        self.tezine = []

    def kruskal_alg(self):

        indeks = list(range(1, int(self.V)+1))
        F = self.grane.copy()
        L = []
        if int(self.V) < 10:
            print("%-55s %-55s %s" % ("Indeks:", "L:", "F:"))
        ispis(self.V, indeks, L, F)

        while len(F):

            u, v = F[0]
            if indeks[u] != indeks[v]:
                maks = max(indeks[u], indeks[v])
                for i, vr in enumerate(indeks):
                    if vr == maks:
                        indeks[i] = min(indeks[u], indeks[v])

                L.append((u, v))
                F.pop(0)
            else:
                F.pop(0)

            ispis(self.V, indeks, L, F)


def ispis(V, indeks, L, F):

    if int(V) < 10:
        print("%-55s %-55s %s" %(indeks, L, F))
    else:
        print("Indeks:", indeks, "\nL:     ", L, "\nF:     ", F)
        print("------")


def unesi_graf():

    V = input("Unesi broj cvorova:")
    graf = Graf(V)
    a = []
    b = []

    for linija in sys.stdin:

        linija = linija.strip().split(" ")
        a.append((int(linija[0]), int(linija[1])))
        b.append(int(linija[2]))

    sortirano = sorted(zip(a, b), key=lambda x: x[1])
    for vr in sortirano:
        graf.grane.append(vr[0])
        graf.tezine.append(vr[1])

    print("\nGrane:", graf.grane, "\nTezine:", graf.tezine, "\n")
    return graf


def main():

    g = unesi_graf()
    g.kruskal_alg()


if __name__ == '__main__':
    main()