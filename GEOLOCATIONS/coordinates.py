import geocoder
#import math
from pathlib import Path
from math import sin, cos, acos, pi, radians
#import pandas 3

def nacteni_souradnic_ze_souboru(file: Path) -> list[tuple]:
    #NACITA SOURADNICE ZE SOUBORU ZADANEM FORMATU A ULOZI JE DO DATOVE STRUKTURY "TUPLE"
    chyby_nszs = Path('data/nacteni_souradnic_ze_souboru_ERR.csv')
    chyby_nszs_pocet = 0
    souradnice : list(tuple) = [] 
    print('ZAHAJUJI NACITANI SOUBORU SOURADNIC: '+str(file))
    if file.exists():
        with open(chyby_nszs, mode='w', encoding = 'utf8') as err0:  
            with open(file, mode='r', encoding = 'utf8') as mf1:
                line = mf1.readline().rstrip() # přečte hlavičku
                line = mf1.readline().rstrip()
                while (line !=''):
                    astr, bstr = line.split(',')
                    lat = float(bstr[1:len(bstr)-1:])
                    #print(lat)
                    line = mf1.readline().rstrip()
                    astr, bstr = line.split(',')
                    lon = float(bstr[1:len(bstr)-1:])
                    #print(lon)
                    try:
                        g = geocoder.osm((lat,lon), method='reverse')
                        souradnice.append((lat,lon))
                        print('('+str(lat)+', '+str(lon)+') > ok')
                    except: # NEZARADI POKUD SESTAVENA SOURADNICE NEPROLEZE GEOKODOVANIM - MUZE BYT NAPR MIMO MEZE
                        chyby_nszs_pocet = chyby_nszs_pocet + 1 
                        print('('+str(lat)+', '+str(lon)+') > NOT ok -> NEZARAZUJI DO SOUBORU SOURADNIC')
                        err0.write('reverse geocoding: ('+str(lat)+';'+str(lon)+'> NOT ok > NEZARAZENO DO DATOVE STRUKTURY'+'\n')    
                    line = mf1.readline().rstrip()
                if chyby_nszs_pocet == 0:
                    err0.write('Pri nacitani souradnic nevznikly zadne vyjimky.')    
            #print(len(souradnice))
            print('SOUBOR SOURADNIC: '+str(file)+' NACTEN > ok')
            print()
    else:
        print(file,'not found')
    return souradnice
    
def nalezeni_dat_k_souradnicim(souradnice:tuple, file: Path) -> None:
    #K SOURADNICIM VE FORMATU TUPLE S POUZITIM SLUZBY GEOGODER NALEZNE UDAJE TYPU ADRESA A ULOZI JE DO SOUBORU file
    chyby_ndks = Path('data/nalezeni_dat_k_souradnicim_ERR.csv')
    chyby_ndks_pocet = 0
    print('ZAHAJUJI REVERZNI GEOKODOVANI (HLEDANI DAT K SOURADNICIM)...')
    with open(file, mode='w', encoding = 'utf8') as of:
        with open(chyby_ndks, mode='w', encoding = 'utf8') as err1:    
            for i in range (0,len(souradnice)):
                try:
                    g = geocoder.osm(souradnice[i], method='reverse')
                    #print(g.osm)
                    #print(souradnice[i])
                    #of.write(str(i+1)+'\n')
                    of.write(str(souradnice[i])+'\n')
                    #print("( "+str(g.osm["y"])+" ; "+str(g.osm["x"])+" )")
                    if "addr:country" in g.osm:
                        #print(g.osm["addr:country"])
                        of.write(str(g.osm["addr:country"])+'\n')
                    if "addr:state" in g.osm:
                        #print(g.osm["addr:state"])
                        of.write(str(g.osm["addr:state"])+'\n')
                    if "addr:city" in g.osm:
                        #print(g.osm["addr:city"])
                        of.write(str(g.osm["addr:city"])+'\n')
                    if "addr:postal" in g.osm:
                        #print(g.osm["addr:postal"])
                        of.write(str(g.osm["addr:postal"])+'\n')
                    if "addr:street" in g.osm:
                        #print(g.osm["addr:street"])
                        of.write(str(g.osm["addr:street"])+'\n')
                    if "addr:housenumber" in g.osm:
                        #print(g.osm["addr:housenumber"])
                        of.write(str(g.osm["addr:housenumber"])+'\n')
                    #print()
                    of.write('\n')
                    print('reverse geocoding: '+str(i)+' > ok')
                except:
                    chyby_ndks_pocet = chyby_ndks_pocet + 1
                    print('reverse geocoding: '+str(i)+' > NOT ok > NEZARAZENO DO DATOVE STRUKTURY')
                    err1.write('reverse geocoding: ('+str(souradnice[i][0])+';'+str(souradnice[i][1])+') > NOT ok > NEZARAZENO DO DATOVE STRUKTURY'+'\n')    
            if chyby_ndks_pocet == 0:
                err1.write('Pri hledani dat k souradnicim nevznikly zadne vyjimky.')
    print('REVERZNI GEOKODOVANI UKONCENO.')
    print('VYSLEDKY JSOU ULOZENY V SOUBORU: '+str(file))
    print()
    return

def nalezeni_souradnic_k_datum(file: Path) -> list[tuple]: 
    #VEZME DATA ZE SEZNAMU MEST A NAJDE K NIM SOURADNICE S POMOCI SLUZBY geocoder; VYSLEDEK ULOZI DO "TUPLE" STRUKTURY SOURADNICE - POPISEK
    chyby_nskd = Path('data/nalezeni_souradnic_k_datum_ERR.csv')
    chyby_nskd_pocet = 0
    print('ZAHAJUJI PRIME GEOKODOVANI (HLEDANI SOURADNIC K DATUM)...')
    souradniceM : list(tuple) = []
    if file.exists():
        with open(chyby_nskd, mode='w', encoding = 'utf8') as err2:
            i = 0
            with open(file, mode='r', encoding = 'utf8') as mf2:
                line = mf2.readline().rstrip() # přečte hlavičku
                line = mf2.readline().rstrip()
                while (line !=''):
                    #print(line)
                    try:
                        g = geocoder.osm(line)
                        souradniceM.append((g.osm['y'],g.osm['x'], line))
                        print('direct geocoding '+str(i)+': '+line+' > ok ')
                    except:
                        chyby_nskd_pocet = chyby_nskd_pocet + 1     
                        print('direct geocoding '+str(i)+': '+line+' > NOT ok > NEZARAZENO DO DATOVE STRUKTURY')
                        err2.write('direct geocoding: '+line+' > NOT ok > NEZARAZENO DO DATOVE STRUKTURY'+'\n') 
                    #print(g.osm['y'])
                    #print(g.osm['x'])
                    i = i + 1
                    line = mf2.readline().rstrip()
            if chyby_nskd_pocet == 0:
                err2.write('Pri hledani souradnic k datum nevznikly zadne vyjimky.')    
        print('PRIME GEOKODOVANI UKONCENO.')
        print('VYSLEDKY JSOU ULOZENY V DATOVE STRUKTURE TUPLE')
        print()
    else:
        print(file,'not found')
    return souradniceM

def nalezeni_nejblizsiho_mesta (souradnice1 : list[tuple], souradniceM : list[tuple], file: Path) -> None:
    #VEZME 2 TUPLES VYTVORENE Z BOU VSTUPNICH SOUBORU; KE KAZDE SOURADNICI Z PRVNIHO ZADANEHO SOUBORU NEZNAMYCH LOKACI
    #SE SANZI NAJIT ORTODROMALNE NEJBLIZSI MESTO ZE SEZNAMU MEST; VYSTUP JE ULOZEN V SOUBORU file
    with open(file, mode='w', encoding = 'utf8') as of2:
        print('ZAHAJUJI HLEDANI NEJBLIZSICH MEST K ZADANYM SOURADNICIM...')
        #print(len(souradnice1))
        #print(len(souradniceM))
        for i in range (0, len(souradnice1)):
            min_vzdalenost = 1000000
            min_index_M = -1
            for j in range (0, len(souradniceM)):
                print(souradnice1[i])
                print('('+str(souradniceM[j][0])+', '+str(souradniceM[j][1])+')')
                vzdalenost = distance(souradnice1[i], souradniceM[j])
                print('ortodromická vzdálenost míst je: '+str(vzdalenost)+' km')
                print()
                if vzdalenost < min_vzdalenost:
                    min_vzdalenost = vzdalenost
                    min_index_M = j
            of2.write('( '+str(souradnice1[i][0])+';'+str(souradnice1[i][1])+' )'+'\n')
            of2.write('Nejblizsi mesto ze seznamu je: '+ souradniceM[min_index_M][2] +'\n')
            of2.write('Vzdalenost: '+str(min_vzdalenost)+' km'+'\n')   
            of2.write('\n')
        print('HLEDANI NEJBLIZSICH MEST K ZADANYM SOURADNICIM UKONCENO.')
        print('VYSLEDKY JSOU ULOZENY V SOUBORU: '+str(file))
        print()    
    return

def distance(bod1: tuple, bod2: tuple) -> float:
    #VRATI ORTODROMALNI VZDALENOST bod1 - bod2 ZADANYCH SOURADNICEMI
    POLOMER_ZEME = 6375 #km    
    u1 = bod1[0]
    v1 = bod1[1]
    u2 = bod2[0]
    v2 = bod2[1]
    cos_c = cos(radians(90-u1))*cos(radians(90-u2))+sin(radians(90-u1))*sin(radians(90-u2))*cos(radians(v2-v1))
    return POLOMER_ZEME * acos(cos_c) # distance in km 

def main() -> None:
    # HLAVNI PROGRAM
    # ze zadaneho souboru nacte koordinaty
    souradnice = nacteni_souradnic_ze_souboru(Path('data\coordinates.csv'))
    # zobrazení souřadnic - jen abychom je viděli, jinak se použijí k dalším krokům bez vizualizace
    print(souradnice) 
    print()
    # k nactenym koordinatum zjisti geoudaje na netu (Open Street Map)
    nalezeni_dat_k_souradnicim(souradnice, Path('data\output1_Ip.csv'))
    # nacte dalsi zadany soubor (mesta) a dohleda k nemu na netu souradnice
    souradniceM = nalezeni_souradnic_k_datum(Path('data\world-cities.csv'))
    # zobrazení souřadnic - jen abychom je viděli, jinak se použijí k dalším krokům bez vizualizace
    print(souradniceM)
    print()
    # ke kazde nezname souradnici ze souboru souradnice najde ortodromalne nejblizsi souradnici se souboru mest
    nalezeni_nejblizsiho_mesta(souradnice,souradniceM, Path('data\output2_Ip.csv'))
    print('geouloha #2 (c) 2022 Ivana Prášilová')
    print()

if __name__ == '__main__':
    main()
    