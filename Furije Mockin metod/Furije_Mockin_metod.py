import numpy

# Funkcija za unos vrednosti
def unesiUlaz(indikator):

    if indikator == 1:
        ulaz = input("Unesite broj nejednacina i broj nepoznatih (oblika Ax <= b, racunajuci i podrazumevane x1>=0...):")
    elif indikator == 2:
        ulaz = input("Unesite broj nejednacina i broj nepoznatih (oblika Ax >= b, NE racunajuci podrazumevane x1>=0...):")

    n = int(ulaz.split(" ")[0])
    m = int(ulaz.split(" ")[1])

    matricaA = numpy.zeros((n, m))
    matricaB = numpy.zeros((n, 1))

    for i in range(n):

        linija = input("Unesite sve koeficijente nejednacine:")
        koefs = list(map(float, linija.split(" ")))

        for j in range(m+1):
            if j == m:
                matricaB[i][0] = koefs[j]
            else:
                matricaA[i][j] = koefs[j]

    return matricaA, matricaB, m


# Funkcija za pronalazenje resenja sistema
def nadjiResenja(niz_matricaA, niz_matricaB, niz_zap_jna, indikator):

    suma_jna_za_oduzimanje = niz_zap_jna[-1]
    stara_suma_jna_za_oduzimanje = 0
    konacno = numpy.array([])
    pom = 1

    while len(niz_zap_jna):

        # U svakoj iteraciji uzimamo jednu eliminantu(sistem nejednacina) od kraja
        nizA = niz_matricaA[len(niz_matricaA)-suma_jna_za_oduzimanje:len(niz_matricaA)-stara_suma_jna_za_oduzimanje, :]
        nizB = niz_matricaB[len(niz_matricaB)-suma_jna_za_oduzimanje:len(niz_matricaA)-stara_suma_jna_za_oduzimanje, :]
        resenja_za_poz = numpy.array([])
        resenja_za_neg = numpy.array([])

        suma_za_proveruA = 0
        suma_za_proveruB = 0

        for i in range(len(nizA)):

            for j in range(len(nizA[0])):
                suma_za_proveruA += nizA[i][j]

            suma_za_proveruB += nizB[i][0]

        # Ako je zbir matrice A = 0 i zbir matrice B = 0 onda prelazimo na prethodnu eliminantu
        if suma_za_proveruA == 0 and suma_za_proveruB == 0:

            niz_zap_jna = niz_zap_jna[:-1]
            stara_suma_jna_za_oduzimanje = suma_jna_za_oduzimanje

            if len(niz_zap_jna):
                suma_jna_za_oduzimanje += niz_zap_jna[-1]

            continue

        # Racunamo intervale
        for u in range(len(nizA)):

            suma = 0

            if len(konacno):
                for h in range(0, len(konacno)):
                    suma += nizA[u][-(h+1)] * konacno[h]

            if nizA[u][-pom] != 0:
                if nizA[u][-pom] > 0:
                    resenja_za_poz = numpy.append(resenja_za_poz, (nizB[u][0] - suma) / nizA[u][-pom])
                elif nizA[u][-pom] < 0:
                    resenja_za_neg = numpy.append(resenja_za_neg, (nizB[u][0] - suma) / nizA[u][-pom])

            if u == len(nizA)-1:
                pom += 1

        if len(resenja_za_neg):

            if len(resenja_za_poz) == 0:
                konacno = numpy.append(konacno, min(resenja_za_neg))
                #print("resenje za min i max:", min(resenja_za_neg), " >= x >= ", "beskonacno")

            elif len(resenja_za_poz):
                konacno = numpy.append(konacno, max(resenja_za_poz))
                #print("resenje za min i max:", min(resenja_za_neg), " >= x >= ", max(resenja_za_poz))

        else:
            if len(resenja_za_poz) == 0:
                konacno = numpy.append(konacno, 1)
                #print("resenje za min i max:", "beskonacno ", " >= x >= ", "beskonacno pa biramo proizvoljno npr. 1")
            else:
                konacno = numpy.append(konacno, max(resenja_za_poz))

        niz_zap_jna = niz_zap_jna[:-1]
        stara_suma_jna_za_oduzimanje = suma_jna_za_oduzimanje

        if len(niz_zap_jna):
            suma_jna_za_oduzimanje += niz_zap_jna[-1]

    if indikator == 1:
        print("Rezultat funkcije cilja: ", konacno[0])
    else:
        print("Konacno resenje (x1, x2...): ", numpy.flip(konacno))


# Funkcija za proveru da li konkretan ulaz pripada resenju
def proveriResenje(matA, matB, tacka):

    konacno = numpy.flip(numpy.array(tacka))
    tacno, netacno = 0, 0

    for u in range(len(matA)):

        suma = 0

        if len(konacno):
            for h in range(0, len(konacno)):
                suma += matA[u][-(h + 1)] * konacno[h]

        if suma >= matB[u][0]:
            tacno += 1
        else:
            netacno += 1

    if netacno == 0:
        print("\n Pripada")
    else:
        print("\n Ne pripada")

    return exit()


# Pomocna funkcija za dodavanje nejednacina iz K
def dodajNejednacineIzK(K, matA, matB, mat2A, mat2B):

    pom_matA = numpy.empty((0, len(matA[0])))
    pom_matB = numpy.empty((0, len(matB[0])))

    for k in K:

        pom_matA = numpy.append(pom_matA, [matA[k]], axis=0)
        pom_matB = numpy.append(pom_matB, [matB[k]], axis=0)

    mat2A = numpy.append(mat2A, pom_matA, axis=0)
    mat2B = numpy.append(mat2B, pom_matB, axis=0)


def main():

    matA = numpy.array([])
    matB = numpy.array([])
    indikator = 0

    f = input("Unesite koeficijente funkcije cilja ili karakter n ako nema:")

    # Ciljnu funkciju prevodimo u oblik f = ... i zamenjujemo u ostalim ogranicenjima
    if f != "n":

        fja = list(map(float, f.split(" ")))
        fja.append(-1)
        indeks = 0

        for i in range(len(fja)):
            if fja[i] != 0:
                indeks = i
                break

        for i in range(len(fja)):
            if i != indeks:
                if fja[i] != 0:
                    fja[i] = fja[i] / (-1*fja[indeks])

        fja[indeks] = 0
        indikator = 1
        ulaz = unesiUlaz(indikator)
        matA = ulaz[0]
        matB = ulaz[1]
        m = ulaz[2]
        nova = numpy.zeros((len(matA), len(fja)))

        for i in range(len(matA)):
            for j in range(len(fja)):
                nova[i][j] = matA[i][indeks] * fja[j]

        pomocna = numpy.zeros((len(matA), 1))
        matA = numpy.append(matA, pomocna, axis=1)
        tmp = numpy.add(matA, nova)
        matA = tmp

        for i in range(len(matA)):
            for j in range(len(matA[0])):
                if j == indeks:
                    matA[i][j] = 0
                else:
                    if i < len(matA)-m:
                        matA[i][j] *= -1

            if i < len(matA) - m:
                matB[i][0] *= -1

        matA = matA[:, 1:]

    # Proveravamo da li zadata tacka pripada resenju
    else:

        indikator = 2
        ulaz = unesiUlaz(indikator)
        matA = ulaz[0]
        matB = ulaz[1]

        ulaznaTacka = input("Unesite tacku za proveru, ako nema unesite karakter n:")

        if ulaznaTacka != "n":

            tacka = list(map(float, ulaznaTacka.split(" ")))
            proveriResenje(matA, matB, tacka)

    # Izvrsavamo sam algoritam
    niz_matricaA = numpy.array(matA)
    niz_matricaB = numpy.array(matB)
    br_vrsta = len(matA)
    br_kolona = len(matA[0])
    niz_zap_jna = numpy.array(br_vrsta)
    i, j, n_novo, ima_resenje = 0, 0, 0, 0

    while j < br_kolona:

        I = []
        J = []
        K = []

        # Gledamo znak vrednosti uz x koje eliminisemo
        for d in range(br_vrsta):
            if matA[d][j] > 0:
                I.append(d)
            elif matA[d][j] < 0:
                J.append(d)
            else:
                K.append(d)

        # Racunamo narednu eliminantu sistema
        if len(I) and len(J):

            n_novo = len(I) * len(J)
            mat2A = numpy.zeros((n_novo, br_kolona))
            mat2B = numpy.zeros((n_novo, 1))
            indeksi = []
            r, t = 0, 0

            for r in I:
                for t in J:
                    indeksi.append([r, t])

            for q in range(n_novo):

                r = indeksi[q][0]
                t = indeksi[q][1]

                for p in range(j + 1, br_kolona):

                    tmp1 = matA[r][p] / matA[r][j] - matA[t][p] / matA[t][j]
                    tmp2 = matB[r][0] / matA[r][j] - matB[t][0] / matA[t][j]

                    # Zaokruzujemo mnogo male vrednosti na 0
                    if numpy.abs(tmp1) < 0.000000001:
                        mat2A[q][p] = 0
                    else:
                        mat2A[q][p] = tmp1

                    if numpy.abs(tmp2) < 0.000000001:
                        mat2B[q][0] = 0
                    else:
                        mat2B[q][0] = tmp2

                # Ako smo izracunali sve nove koeficijente pamtimo novu matricu i prelazimo na sledecu
                if q == n_novo-1:

                    # Dodamo i nejednacine iz K
                    if len(K):
                        dodajNejednacineIzK(K, matA, matB, mat2A, mat2B)

                    niz_matricaA = numpy.append(niz_matricaA, mat2A, axis=0)
                    niz_matricaB = numpy.append(niz_matricaB, mat2B, axis=0)
                    matA = mat2A
                    matB = mat2B

                    br_vrsta = len(matA)
                    niz_zap_jna = numpy.append(niz_zap_jna, br_vrsta)

        elif len(K):
                dodajNejednacineIzK(K, matA, matB, mat2A, mat2B)

        elif (len(I) == 0 and len(K) == 0) or (len(J) == 0 and len(K) == 0):
            ima_resenje = 1

        # Zavrsena eliminacija svih promenljivih, proveravamo da li ima resenja i trazimo ako ima
        if j == br_kolona - 1:

            tacno = 0
            netacno = 0

            # Proveravamo da li su sve nejednacine u poslednjoj eliminanti ispravne
            for l in range(len(mat2A)):
                if numpy.sum(mat2A[l][:]) >= mat2B[l][0]:
                    tacno += 1
                else:
                    netacno += 1

            if netacno == 0:
                print("\n Sistem ima resenja")
                ima_resenje = 1
            else:
                ima_resenje = 0
                print("\n Sistem nema resenja")

            if ima_resenje == 1:
                nadjiResenja(niz_matricaA, niz_matricaB, niz_zap_jna, indikator)

            exit()

        j += 1


if __name__ == '__main__':
   main()
