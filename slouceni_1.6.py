import glob
from os import path, _exit
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
from datetime import datetime
from time import asctime
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


cesta_k_souborum = "U:/AV_Beku/Projekty/Slouceni_korektur/cesta_k_souborum_nemazat_pouze_prepsat.txt" # Cesta k souborovému adresáři
cesta_k_licenci = "U:/AV_Beku/Projekty/Slouceni_korektur/licence.stj"


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

def priprav_klic():
    heslo = "PyladiesPlzen"
    salt = b"/*-*/"
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
    )
    klic = base64.urlsafe_b64encode(kdf.derive(heslo.encode()))
    return klic


def odkoduj_zaznamy(klic):
    with open(cesta_k_licenci, mode="r", encoding="utf-8") as expirace:
        expirace = expirace.read()
        try:
            f = Fernet(klic)
            expirace = ((f.decrypt(expirace.encode()).decode("utf-8")))
            return expirace
        except:
            print("Poškozený licenční soubor")
            input("Ukončuji program")
            _exit(0)

def overeni_licence(expirace):
    if expirace[-3:] != "PDF":
        print("Licence není pro tento program.")
        input("Ukončuji program")
        _exit(0)

    pocet_carek = 0
    rok = ""
    mesic = ""
    den = ""
    for ii in expirace:
        if ii != ",":
            if pocet_carek == 0:
                rok = rok + ii
            elif pocet_carek == 1:
                mesic = mesic + ii
            elif pocet_carek == 2:
                den = den + ii
            else:
                break
        else:
            pocet_carek = pocet_carek + 1

    systemovy_cas = asctime()
    systemovy_cas = systemovy_cas.replace("  ", " ")

    mezera = 0
    mesic_akt = ""
    den_akt = ""
    rok_akt = ""

    for qq in systemovy_cas:
        if qq == " ":
            mezera = mezera + 1
        elif qq != " ":
            if mezera == 0:
                pass
            elif mezera == 1:
                mesic_akt = mesic_akt + qq
            elif mezera == 2:
                den_akt = den_akt + qq
            elif mezera == 3:
                pass
            else:
                rok_akt = rok_akt + qq

    if mesic_akt == "Jan":
        mesic_akt = "1"
    elif mesic_akt == "Feb":
        mesic_akt = "2"
    elif mesic_akt == "Mar":
        mesic_akt = "3"
    elif mesic_akt == "Apr":
        mesic_akt = "4"
    elif mesic_akt == "May":
        mesic_akt = "5"
    elif mesic_akt == "Jun":
        mesic_akt = "6"
    elif mesic_akt == "Jul":
        mesic_akt = "7"
    elif mesic_akt == "Aug":
        mesic_akt = "8"
    elif mesic_akt == "Sep":
        mesic_akt = "9"
    elif mesic_akt == "Oct":
        mesic_akt = "10"
    elif mesic_akt == "Nov":
        mesic_akt = "11"
    elif mesic_akt == "Dec":
        mesic_akt = "12"


    d1 = datetime(int(rok), int(mesic), int(den))
    d2 = datetime(int(rok_akt), int(mesic_akt), int(den_akt))
    rozdil = d1 - d2
    rozdil = str(rozdil)
    pocet_dnu = ""
    for aa in rozdil:
        if aa == " ":
            break
        else:
            pocet_dnu += aa

    if pocet_dnu == "0:00:00":
        print("POZOR vaše licence dnes vyprší!!")
        return True
    elif int(pocet_dnu) > 30:
        print("Do konce licence zbývá", pocet_dnu, "dnů.")
        return True
    elif (int(pocet_dnu) <= 30) and (int(pocet_dnu) > 0):
        print("POZOR vaše licence vyprší za", pocet_dnu, "dnů!!")
        print("Po tomto datu nebude program fungovat.")
        return True
    else:
        print("Vaše licence vypršela, požádejte správce o nový licenční soubor.")
        return False


klic = priprav_klic()
expirace = odkoduj_zaznamy(klic)
overeni_licence(expirace)



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