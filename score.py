
import random
import os

def generate_score_aviz(nr_puncte_lucru_aviz:int,activitati_aviz:list,nr_prod_aviz:int,nr_grupe_aviz:int) -> int:
    score = 5
    if "S" in activitati_aviz:
        score += 5
    score += nr_prod_aviz + nr_grupe_aviz * 5 + nr_puncte_lucru_aviz
    return score

def generate_score_anexa(adaugare_puncte_lucru_anexa:int,adaugare_activitati_anexa:list,
                              adaugare_nr_prod_anexa:int,adaugare_nr_grupe_anexa:int,schimbare_denumire_sediu_social:str,
                              schimbare_denumire_firma:str,radiere_activitate:str,radiere_puncte_lucru:str,radiere_producatori:str) -> int:
    score = 2
    if len(adaugare_activitati_anexa) > 0:
        score += 5
        if len(adaugare_activitati_anexa) >1 and "S" in adaugare_activitati_anexa:
            score += 5
    score += adaugare_nr_prod_anexa + adaugare_nr_grupe_anexa * 5 + adaugare_puncte_lucru_anexa + [schimbare_denumire_sediu_social, schimbare_denumire_firma, radiere_activitate, radiere_puncte_lucru, radiere_producatori].count("DA")
    return score

# Generare automata de cazuri pentru cele doua functii

if __name__ == "__main__":
    tip_cerere = random.choice(["aviz", "anexa"])
    if tip_cerere == "aviz":
        nr_puncte_lucru_aviz = random.randint(1, 10) # Just test purposes, can be any number really
        activitati_aviz = set(random.sample(['I', 'D', 'S'], random.randint(1,3)))
        if "I" not in activitati_aviz and "D" not in activitati_aviz:
            nr_prod_aviz = 0
        else:
            nr_prod_aviz = random.randint(1,10) # Just test purposes, can be any number really
        if "S" not in activitati_aviz:
            nr_grupe_aviz = 0
        else:
            nr_grupe_aviz = random.randint(1,10) # Just test purposes, can be any number really
        os.system('cls' if os.name == 'nt' else 'clear') # 'clear' instead of cls on linux/mac
        print(f"{str.capitalize(tip_cerere)}\n{[i for i in activitati_aviz]}\n{nr_puncte_lucru_aviz} PUNCTE DE LUCRU\n{nr_prod_aviz} PRODUCATORI\n{nr_grupe_aviz} GRUPE SERVICE")
        get_score=generate_score_aviz(nr_puncte_lucru_aviz,activitati_aviz,nr_prod_aviz,nr_grupe_aviz)
        print(f"Punctaj total: {get_score}")
    else:
        adaugare_puncte_lucru_anexa = random.randint(1, 10)
        adaugare_activitati_anexa = set(random.sample(['I', 'D', 'S'], random.randint(0,2))) # poate sa nu adauge nici o activitate
        if "I" in adaugare_activitati_anexa or "D" in adaugare_activitati_anexa:
            adaugare_nr_prod_anexa = random.randint(1,10) # Daca adauga import sau distributie trebuie neaparat sa adauge si producatori
        else:
            adaugare_nr_prod_anexa = random.randint(0,10) # Daca nu, adaugare_nr_prod_anexa poate fi si 0, dar poate fi si orice alt numar (adauga activitatea de service si adauga un nr de producatori pentru activitatea preexistenta de I/D)
        if "S" in adaugare_activitati_anexa:
            adaugare_nr_grupe_anexa = random.randint(1,10) # Daca adauga service, trebuie sa adauge cel putin o grupa de DM
        else:
            adaugare_nr_grupe_anexa = random.randint(0,10) # Daca nu, valoarea poate fi si 0
        schimbare_denumire_sediu_social = random.choice(["DA", "NU"])
        schimbare_denumire_firma = random.choice(["DA", "NU"])
        radiere_activitate = random.choice(["DA", "NU"])
        radiere_puncte_lucru = random.choice(["DA", "NU"])
        radiere_producatori = random.choice(["DA", "NU"])
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{str.capitalize(tip_cerere)}\nADAUGA {[i for i in adaugare_activitati_anexa]}\n{adaugare_puncte_lucru_anexa} PUNCTE LUCRU\n{adaugare_nr_prod_anexa} PRODUCATORI\n{adaugare_nr_grupe_anexa} GRUPE\n{schimbare_denumire_sediu_social}-SCHIMBA DENUMIRE SEDIU SOCIAL\n{schimbare_denumire_firma}-SCHIMBA DENUMIRE FIRMA\n{radiere_activitate}-RADIAZA ACTIVITATE\n{radiere_puncte_lucru}-RADIAZA PUNCTE LUCRU\n{radiere_producatori}-RADIAZA PRODUCATORI")
        get_score = generate_score_anexa(adaugare_puncte_lucru_anexa,adaugare_activitati_anexa,adaugare_nr_prod_anexa,adaugare_nr_grupe_anexa,schimbare_denumire_sediu_social,schimbare_denumire_firma,radiere_activitate,radiere_puncte_lucru,radiere_producatori)
        print(f"Punctaj total: {get_score}")
        
