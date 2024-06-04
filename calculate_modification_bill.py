import random
import os

def generate_modification_valid_tests():
    workplaces = {}
    change_company_name = random.choice(["DA", "NU"])
    change_nonactivity_hq = random.choice(["DA", "NU"])
    add_workplace = random.randint(1, 25)
    delete_workplace = random.randint(1, 10)
    add_activity = random.choice(["DA", "NU"])
    add_manufacturers = random.randint(1, 150)
    add_groups = random.randint(1, 75)
    delete_manufacturers = random.randint(1, 20)
    workplaces_nr = random.randint(1, 2)  # Number of workplaces with new activities can be 2

    if add_activity == "DA":
        for i in range(workplaces_nr):
            workplace_key = f"Punct de lucru {i}"
            workplaces[workplace_key] = [
                random.choice(["DA", "NU"]),
                random.choice(["DA", "NU"]),
                random.choice(["DA", "NU"])
            ]
            if "DA" not in workplaces[workplace_key]:
                workplaces[workplace_key][random.randint(0, 2)] = "DA"
            if all(activity =="DA" for activity in workplaces[workplace_key]):
                workplaces[workplace_key][random.randint(0, 2)] = "NU"
        
        # Check conditions outside the loop
        service_has_no_da = all(value[2] == "NU" for value in workplaces.values())
        import_distribution_has_no_da = all(value[0] == "NU" and value[1] == "NU" for value in workplaces.values())
        if service_has_no_da:
            add_groups = 0  # Set to 0 if no "DA" is found in the third element
        if import_distribution_has_no_da:
            add_manufacturers = 0  # Set to 0 if no "DA" is found in the first two elements
        
        if workplaces_nr == 2:
            if workplaces["Punct de lucru 0"][0] == "DA" and workplaces["Punct de lucru 1"][0] == "DA":
                workplaces["Punct de lucru 1"][0] = "NU"
            if workplaces["Punct de lucru 0"][1] == "DA" and workplaces["Punct de lucru 1"][1] == "DA":
                workplaces["Punct de lucru 1"][1] = "NU"
            if workplaces["Punct de lucru 0"][2] == "DA" and workplaces["Punct de lucru 1"][2] == "DA":
                workplaces["Punct de lucru 1"][2] = "NU"

    os.system('cls' if os.name == 'nt' else 'clear')
    return change_company_name, change_nonactivity_hq, add_workplace, delete_workplace, add_activity, add_manufacturers, add_groups, delete_manufacturers, workplaces

if __name__ == "__main__":
    change_company_name, change_nonactivity_hq, add_workplace, delete_workplace, add_activity, add_manufacturers, add_groups, delete_manufacturers, workplaces = generate_modification_valid_tests()
    print(f"Schimba numele firmei: {change_company_name}")
    print(f"Schimba sediul social fara activitate: {change_nonactivity_hq}")
    print(f"Adauga puncte de lucru: {add_workplace}")
    print(f"Radiaza punct de lucru: {delete_workplace}")
    print(f"Adauga activitate: {add_activity}")
    if add_activity == "DA":
        for workplace, activities in workplaces.items():
            print(f"{workplace}: {activities}")
    print(f"Adauga producatori: {add_manufacturers}")
    print(f"Radiaza producatori: {delete_manufacturers}")
    print(f"Adauga grupe service: {add_groups}")