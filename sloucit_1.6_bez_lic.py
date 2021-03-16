import glob
from os import path, _exit
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter


cesta_k_souborum = "cesta_k_souborum_nemazat_pouze_prepsat.txt" # Cesta k souborovému adresáři


def sloucit(i, m, o):
    """
    Sloučení PDF souborů
    """
    merger = PdfFileMerger()
    merger.append(PdfFileReader(i), "rb")
    merger.append(PdfFileReader(m), "rb")
    merger.write(o)

def venek_soubory(c_zakazky):
    """
    Projde adresář v venkovním tiskem a odfiltruje nežádoucí soubory.
    Ponechá soubory pouze s koncovkou .pdf a vrátí je.
    """

    try:
        with open(cesta_k_souborum, encoding="utf-8") as f1:
            f1 = f1.read()
    except FileNotFoundError:
        print("Cesta k venkovním souborům nenalezena.")
        print("Ukončuji program")
        input()
        os._exit(0)

    f1_cesta = f1 + c_zakazky + "/"
    f1_soubory = glob.glob(path.join(f1_cesta, "*.pdf"))
#   print(f1_soubory)
    return f1_soubory


def cesta_vnitrek_soubory(c_zakazky):
    """
    Projde adresář v venkovním tiskem a odfiltruje nežádoucí soubory.
    Ponechá soubory pouze s koncovkou .pdf a vrátí je.
    """

    try:
        with open(cesta_k_souborum, encoding="utf-8") as f2:
            f2 = f2.read()
        f2_cesta = f2 + c_zakazky + "/ID/"
        f2_soubory = glob.glob(path.join(f2_cesta, "*.pdf"))
    except FileNotFoundError:
        print("Cesta k vnitřním souborům nenalezena.")
        print("Vnitřní tisk nebude přidružen")
        input()
        a = ""
        return a
#    print(f2_soubory)
    return f2_soubory

def cesta_vnitrek_soubory_lak(c_zakazky):
    """
    Projde adresář v venkovním tiskem a odfiltruje nežádoucí soubory.
    Ponechá soubory pouze s koncovkou .pdf a vrátí je.
    """

    try:
        with open(cesta_k_souborum, encoding="utf-8") as f2:
            f2 = f2.read()
        f2_cesta = f2 + c_zakazky + "/Lak/"
        f2_soubory = glob.glob(path.join(f2_cesta, "*.pdf"))
    except FileNotFoundError:
        print("Cesta k vnitřním souborům nenalezena.")
        print("Laková forma nebude přidružena")
        input()
        b = ""
        return b
#    print(f2_soubory)
    return f2_soubory


def sloucit_vnitrek(c_zakazky):
    """
    Vlastní chod programu
    """

    print()
    print("Čekej, dávám dohromady vnitřní tisk.")
    vstup_venkovni_soubory = venek_soubory(c_zakazky)
    vstup_vnitrni_soubory = cesta_vnitrek_soubory(c_zakazky)
    # f3 = venek_soubory(zakazka)

    slouceno = 0
    for i in vstup_venkovni_soubory:
        nazev_souboru = i.split()
        nazev_souboru = i.replace("-", "_").replace("_", " ").replace(",", "").replace(".pdf", " ")
        nazev_souboru = nazev_souboru.lower()
        if ("lack" in nazev_souboru) or ("lak" in nazev_souboru):
            pass
        else:
            nalezeno = False
            a = i[23:] # vrátit 23
            a = a.replace("-", "_").replace("_", " ").replace(",", "")
            a = a.lower()
    #       print(a)
            for m in vstup_vnitrni_soubory:
                m = m.lower()
                n = m.replace("-", "_").replace("_", " ").replace(",", "").replace(".pdf", " ")
    #           print(n)
                if a[10:13] in n:
    #                print(a)
                    o = i
                    try:
                        sloucit(i, m, o)
                    except PermissionError:
                        print("Cílový soubor je otevřen jiným uživatelem")
                        print("Ukončuji program")
                        input()
                        os._exit(0)
                    slouceno += 1
                    print(a[10:13], "    Vnitřek sloučeno")
                    nalezeno = True
                    break
                else:
                    pass
            if nalezeno == False:
                print(a[10:13], "    Vnitřek NESLOUČENO!!!!")
    print()
    print("Celkem sloučeno", slouceno, "souborů.")
    print()
    print("Hotovo")
    input()

def sloucit_lak(c_zakazky):
    """
    Vlastní chod programu
    """

    print()
    print("Čekej, dávám dohromady lak.")
    vstup_venkovni_soubory = venek_soubory(c_zakazky)
    vstup_vnitrni_soubory = cesta_vnitrek_soubory_lak(c_zakazky)
    # f3 = venek_soubory(zakazka)

    slouceno = 0
    for i in vstup_venkovni_soubory:
        nazev_souboru = i.split()
        nazev_souboru = i.replace("-", "_").replace("_", " ").replace(",", "").replace(".pdf", " ")
        nazev_souboru = nazev_souboru.lower()
        if ("lack" in nazev_souboru) or ("lak" in nazev_souboru):
            pass
        else:
            nalezeno = False
            a = i[23:]
            a = a.replace("-", "_").replace("_", " ").replace(",", "")
    #       print(a)
            for m in vstup_vnitrni_soubory:
                n = m.replace("-", "_").replace("_", " ").replace(",", "").replace(".pdf", " ")
    #           print(n)
                if a[10:13] in n:
    #                print(a)
                    o = i
                    try:
                        sloucit(i, m, o)
                    except PermissionError:
                        print("Cílový soubor je otevřen jiným uživatelem")
                        print("Ukončuji program")
                        input()
                        os._exit(0)
                    slouceno += 1
                    print(a[10:13], "    Lak sloučeno")
                    nalezeno = True
                    break
                else:
                    pass
            if nalezeno == False:
                print(a[10:13], "    Lak NESLOUČENO!!!!")
    print()
    print("Celkem sloučeno", slouceno, "souborů.")
    print()
    print("Hotovo")
    input()



while True:
    # overeni()
    c_zakazky = input("Zadej číslo zakázky. ")
    otazka = input("Je zakázkové číslo správně? a/n: ")
    print()
    if otazka == "a":
        sloucit_vnitrek(c_zakazky)
        otazka_lak = input("Chceš připojit lakovou formu? a/n: ")
        if otazka_lak == "a":
            sloucit_lak(c_zakazky)
            break
        else:
            print("Lak nebude přidružen.")
            input()
            break
    else:
        print("Takže znovu")