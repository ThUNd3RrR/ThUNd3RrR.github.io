import random
import os
import json
from fpdf import FPDF

os.environ["PYTHONUTF8"] = "1"

class PDF(FPDF):
    def header(self):
        # Add the header image
        self.image('HEADER.jpg', 0, 0, 210)  # Adjust the width as needed
        self.set_y(30)  # Set the y position below the image
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Fee Calculation Report', 0, 1, 'C')
        self.ln(10)  # Add some space after the header title
        # Add the watermark image (to be behind the text)
        self.image('WATERMARK.jpg', 6, 50, 200, 200)  # Position the watermark and adjust size

    def footer(self):
        self.set_y(-20)  # Position the footer 20 units from the bottom
        # Add the footer image
        self.image('Footer.jpg', 0, self.get_y(), 210, 3)  
        self.set_y(-15)  # Adjust y position to be above the footer image
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 3, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 5, body)  # Adjust the line height as needed
        self.ln()

def load_fees_rules(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['fees'], data['Additional rules']

def calculate_fee(fees, rules, import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups):
    total_fee = 0
    explanations = []
    multiple_activities_discount_applied = False

    # Calculate import/distribution fee
    if import_wp > 0 or distribution_wp > 0:
        for fee in fees:
            if fee['category'] == "import_or_distribution":
                explanations.append(f"\n{fee['description']}")
                for threshold in fee.get('thresholds', []):
                    if manufacturers <= (threshold.get('max_producers') or float('inf')):
                        import_distribution_fee = threshold['fee']
                        total_fee += import_distribution_fee
                        explanations.append(f"     {threshold['description']}: {import_distribution_fee}")
                        break
    
    # Calculate fees for services
    if service_wp > 0:
        for fee in fees:
            if fee['category'] == "Service":
                explanations.append(f"\n{fee['description']}")
                for threshold in fee.get('thresholds', []):
                    if groups <= (threshold.get('max_groups') or float('inf')):
                        service_fee = threshold['fee']
                        total_fee += service_fee
                        explanations.append(f"     {threshold['description']}: {service_fee}")
                        break
                    
    # 6(3) Logic. Import + Distribution
    if import_wp > 0 and distribution_wp > 0:
        for rule in rules:
            if rule.get('rule') == "multiple_activities_discount" and not multiple_activities_discount_applied:
                total_fee += import_distribution_fee * rule['multiplier']
                explanations.append(f"\n{rule['description']}: {import_distribution_fee * rule['multiplier']}")
                multiple_activities_discount_applied = True
                break

    # 6(4) Logic
    if import_only_wp >1 or distribution_wp >1 or service_wp >1:
        multiple_workplaces_discount = []
        for rule in rules:
            if rule['rule'] == "multiple_workplaces_discount":
                explanations.append(f"\n{rule['description']}")
                for treshold in rule.get('tresholds',[]):
                    multiple_workplaces_discount.append(treshold['multiplier'])

        if import_only_wp > 1:
            for rule in rules:
                for treshold in rule.get('tresholds',[]):
                    if import_only_wp >10: 
                        additional_import_fee_50 = 9 * multiple_workplaces_discount[0] * import_distribution_fee   
                        additional_import_fee_25 = (import_only_wp - 10) * multiple_workplaces_discount[1] * import_distribution_fee
                        total_fee += additional_import_fee_50 + additional_import_fee_25
                        explanations.append(f"\n     {import_only_wp - 1} punct(e) de lucru cu import tarifate aditional din care :")
                        explanations.append(f"     a) 9 puncte de lucru cu import tarifate 50% : {additional_import_fee_50}")
                        explanations.append(f"     b) {import_only_wp - 10} punct(e) de lucru cu import tarifate 25% : {additional_import_fee_25}")
                        break
                    else:
                        additional_import_fee_50 = (import_only_wp - 1) * multiple_workplaces_discount[0] * import_distribution_fee  
                        total_fee += additional_import_fee_50
                        explanations.append(f"\n     {import_only_wp - 1} punct(e) de lucru cu import tarifate aditional din care :")
                        explanations.append(f"     a) {import_only_wp - 1} punct(e) de lucru cu import tarifate 50% : {additional_import_fee_50}")
                        break
                            
        if distribution_wp > 1:
            for rule in rules:
                for treshold in rule.get('tresholds',[]):
                    if distribution_wp >10: 
                        additional_import_fee_50 = 9 * multiple_workplaces_discount[0] * import_distribution_fee   
                        additional_import_fee_25 = (distribution_wp - 10) * multiple_workplaces_discount[1] * import_distribution_fee
                        total_fee += additional_import_fee_50 + additional_import_fee_25
                        explanations.append(f"\n     {distribution_wp - 1} punct(e) de lucru cu distributie tarifate aditional din care :")
                        explanations.append(f"     a) 9 puncte de lucru cu distributie tarifate 50% : {additional_import_fee_50}")
                        explanations.append(f"     b) {distribution_wp - 10} punct(e) de lucru cu distributie tarifate 25% : {additional_import_fee_25}")
                        break
                    else:
                        additional_import_fee_50 = (distribution_wp - 1) * multiple_workplaces_discount[0] * import_distribution_fee  
                        total_fee += additional_import_fee_50
                        explanations.append(f"\n     {distribution_wp - 1} punct(e) de lucru cu distributie tarifate aditional din care :")
                        explanations.append(f"     a) {distribution_wp - 1} punct(e) de lucru cu distributie tarifate 50% : {additional_import_fee_50}")
                        break

        if service_wp > 1:
            for rule in rules:
                for treshold in rule.get('tresholds',[]):
                    if service_wp >10: 
                        additional_service_fee_50 = 9 * multiple_workplaces_discount[0] * service_fee   
                        additional_service_fee_25 = (service_wp - 10) * multiple_workplaces_discount[1] * service_fee
                        total_fee += additional_service_fee_50 + additional_service_fee_25
                        explanations.append(f"\n     {service_wp - 1} punct(e) de lucru cu service tarifate aditional din care :")
                        explanations.append(f"     a) 9 puncte de lucru cu service tarifate 50% : {additional_service_fee_50}")
                        explanations.append(f"     b) {service_wp - 10} punct(e) de lucru cu service tarifate 25% : {additional_service_fee_25}")
                        break
                    else:
                        additional_service_fee_50 = (service_wp - 1) * multiple_workplaces_discount[0] * service_fee 
                        total_fee += additional_service_fee_50
                        explanations.append(f"\n     {service_wp - 1} punct(e) de lucru cu service tarifate aditional din care :")
                        explanations.append(f"     a) {service_wp - 1} punct(e) de lucru cu service tarifate 50% : {additional_service_fee_50}")
                        break
    for fee in fees:
        if fee['category'] == "issue_permit_or_annex":
            total_fee += fee['fee']
            explanations.append(f"\n{fee['description']}: {fee['fee']}")

    return explanations, total_fee
  
# Generate valid test cases
def generate_permit_valid_tests():
    workplaces = {}
    nr_workplaces = random.randint(1,19)
    for i in range(1, nr_workplaces+1):
        workplace_key = f"Punct de lucru {i}"
        workplaces[workplace_key] = [
            random.choice(["DA","NU"]),
            random.choice(["DA","NU"]),
            random.choice(["DA","NU"])
        ]
        if "DA" not in workplaces[workplace_key]:
            workplaces[workplace_key][random.randint(0, 2)] = "DA"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"     AVIZ {10 * ' '} I    D     S")
    print(f"{36 * '-'}")
    for key, value in workplaces.items():
        print(f"{key}: {value}")
    print("\n")
    manufacturers = random.randint(1,300) # Can be any number
    groups = random.randint(1,100) 
    service_has_no_da = all(value[2] == "NU" for value in workplaces.values())
    import_distribution_has_no_da = all(value[0] == "NU" and value[1] == "NU" for value in workplaces.values())
    if service_has_no_da:
        groups = 0  # Set to 0 if no "DA" is found in the third element
    if import_distribution_has_no_da:
        manufacturers = 0  # Set to 0 if no "DA" is found in the first two elements
    print(f"Manufacturers: {manufacturers}\nGroups: {groups}\n")
    import_only_wp = [value[0] for value in workplaces.values() if value[1] =="NU" and value[2] == "NU"].count("DA")
    import_wp = [value[0] for value in workplaces.values()].count("DA")
    distribution_wp = [value[1] for value in workplaces.values()].count("DA")
    service_wp = [value[2] for value in workplaces.values()].count("DA")
    print(f"Import Workplaces: {import_wp}\nImportOnly: {import_only_wp}\nDistribution Workplaces: {distribution_wp}\nService Workplaces: {service_wp}\n")
    return import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups, workplaces

def format_dictionary_data(dictionary):
    formatted_data = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            formatted_data += f"{key}:\n"
            formatted_data += format_dictionary_data(value)
        else:
            formatted_data += f"{key}: {value}\n"
    return formatted_data

def save_to_pdf(explanations, total, workplaces, import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups, filename="report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Workplaces table")
    pdf.chapter_body(f"{workplaces}")
    pdf.chapter_title("Summary")
    pdf.chapter_body(f"Manufacturers: {manufacturers}\nGroups: {groups}\nImport Workplaces: {import_wp}\nImport Only Workplaces: {import_only_wp}\nDistribution Workplaces: {distribution_wp}\nService Workplaces: {service_wp}")
    pdf.chapter_title("Fee Calculation Breakdown")
    pdf.chapter_body("\n".join(explanations))
    pdf.chapter_title("Total Fee")
    pdf.chapter_body(f"Cost servicii evaluare: {total}")
    pdf.output(filename)
    print(f"Report saved as {filename}")

if __name__ == "__main__":
    import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups, workplaces = generate_permit_valid_tests()
    file_path = r"C:\Users\ThUnd3R\tarifare\fees.json"
    fees, rules = load_fees_rules(file_path)
    explanations, total = calculate_fee(fees, rules, import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups)
    for i in range(len(explanations)):
        print(explanations[i])
    print(f"\nCost servicii evaluare: {total}\n")
    formatted_workplaces = format_dictionary_data(workplaces)
    save_to_pdf(explanations, total, formatted_workplaces, import_wp, import_only_wp, distribution_wp, service_wp, manufacturers, groups)
    