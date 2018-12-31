import sys


class Graf:

    def __init__(self):
        self.grane = []
        self.tok = []
        self.kapacitet = []
        self.izvor = 0
        self.ponor = 0

    def dodaj_granu(self, u, v):
        self.grane.append((u, v))

    def dodaj_tok_kapacitet(self, t, k):
        self.tok.append(t)
        self.kapacitet.append(k)

    # Edmonds-Karp modifikacija
    def ford_fulkerson_modif(self):
        iteracija = 1

        while 1:

            print("\nIteracija:", iteracija)
            iteracija += 1

            # S je lista sa elementima oblika (pocetak, kraj grane, orjentacija, maksimalna popravka grane)
            S = [(self.izvor, None, None, float('+inf'))]
            L = [self.izvor]
            S2 = [S[0][0]]  # Pomocna lista koja sadrzi nazive cvorova
            print("S:", S2, "L:", L)

            # Dok ne ispraznimo L uzimamo glavu od L i indeksiramo njegove susede
            while L:

                # Citamo glavu od L
                u = L[0]

                if u == self.ponor:
                    break

                # Za cvor u obradjujemo njegove susede
                for v in zip(self.grane, self.tok, self.kapacitet):

                    # Ako je u pocetak grane i kraj grane nije u skupu S dodaj ga i obradi
                    if v[0][0] == u and v[0][1] not in S2:
                        if v[1] < v[2]:

                            # Trazimo mogucu popravku za prethodnika
                            pret = [x[3] for x in S if x[1] == u]
                            if not pret:
                                pret = [float('+inf')]

                            # Trazimo minimum izmedju maksimalne popravke trenutne grane i prethodne
                            p = min(v[2] - v[1], pret[0])
                            S.append((v[0][0], v[0][1], "+", p))  # Direktna grana pa je znak "+"
                            S2.append(v[0][1])
                            L.append(v[0][1])

                            print("S:", S2, " L:", L)

                    # Ako je u kraj grane i pocetak grane nije u S dodaj ga i obradi
                    elif v[0][1] == u and v[0][0] not in S2:
                        if v[1] > 0:

                            pret = [x[3] for x in S if x[1] == u]
                            if not pret:
                                pret = [float('+inf')]

                            p = min(v[1], pret[0])
                            S.append((v[0][1], v[0][0], "-", p))  # Indirektna grana pa je znak "-"
                            S2.append(v[0][0])
                            L.append(v[0][0])

                            print("S:", S2, " L:", L)

                L.pop(0)
                print("S:", S2, " L:", L)

            # Ako je ispraznjen L ispisujemo max protok, STOP
            if not L:
                print("\nMaksimalni protok:", sum([self.tok[self.grane.index(x)] for x in self.grane if x[0] == self.izvor]))
                exit()

            k = [x for x in S if x[1] == self.ponor]
            poboljsanje = k[0][3]

            k = k[0]
            put = [k]
            for m in list(reversed(S)):
                if m[1] == put[-1][0]:
                    put.append(m)

                if m[2] is None:
                    break

            # Poboljsavamo trenutni tok
            put = list(reversed(put))
            put_pom = [(x[0], x[1]) for x in put]

            for grana in self.grane:
                if grana in put_pom:

                    indeks = put_pom.index(grana)
                    znak = put[indeks][2]
                    if znak == "+":
                        ind = self.grane.index(grana)
                        self.tok[ind] += poboljsanje

                elif tuple(reversed(grana)) in put_pom:

                    indeks = put_pom.index(tuple(reversed(grana)))
                    znak = put[indeks][2]
                    if znak == "-":
                        ind = self.grane.index(grana)
                        self.tok[ind] -= poboljsanje

            # Ispis za tekucu iteraciju
            print("Put:", put_pom, ", poboljsanje:", poboljsanje)
            tok = [self.tok[i] for i, x in enumerate(self.grane) if x in put_pom or tuple(reversed(x)) in put_pom]
            print("Tok: ", end="")
            for i in tok:
                print("{:^7d}".format(i), end=" ")
            print()


def unesi_graf():

    l = input("Unesi izvor i ponor:").split(" ")
    graf = Graf()
    graf.izvor = int(l[0])
    graf.ponor = int(l[1])

    for linija in sys.stdin:

        linija = linija.strip().split(" ")
        graf.dodaj_granu(int(linija[0]), int(linija[1]))
        graf.dodaj_tok_kapacitet(int(linija[2]), int(linija[3]))

    return graf


def main():

    g = unesi_graf()
    print("\nGrane:    ", g.grane, "\nTok:      ", g.tok, "\nKapacitet:", g.kapacitet)

    g.ford_fulkerson_modif()


if __name__ == '__main__':
    main()