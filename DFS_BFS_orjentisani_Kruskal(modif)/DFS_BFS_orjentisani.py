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


if __name__ == '__main__':
    main()