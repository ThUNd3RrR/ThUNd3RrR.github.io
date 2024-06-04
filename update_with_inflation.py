import json

def load_fees_rules(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def custom_round(value):
    # Check the decimal part of the value, if it's 0.5 or more, round up, otherwise round down
    if (value - int(value)) >= 0.5:
        return int(value) + 1
    else:
        return int(value)

def update_fees_with_inflation(data, inflation_rate):
    # Update fees within each category
    for category in data['fees']:
        if 'thresholds' in category:
            for threshold in category['thresholds']:
                threshold['fee'] = custom_round(round(threshold['fee'] * (1 + inflation_rate), 2))
        else:
            # Directly updating fees that are not under thresholds but are directly under category
            if 'fee' in category:
                category['fee'] = custom_round(round(category['fee'] * (1 + inflation_rate), 2))

    # Optionally update other rules or values if needed
    # For example, if additional rules have fee components:
    for rule in data['Additional rules']:
        if 'multiplier' in rule:
            # Assuming you might want to adjust multipliers too
            rule['multiplier'] = custom_round(round(rule['multiplier'] * (1 + inflation_rate), 2))

    return data

def save_updated_fees(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    file_path = r"C:\Users\ThUnd3R\fees.json"
    inflation_rate = 0.104  # Example: 3% inflation

    # Load, update, and save back to file
    fees_data = load_fees_rules(file_path)
    updated_fees_data = update_fees_with_inflation(fees_data, inflation_rate)
    save_updated_fees(file_path, updated_fees_data)
    print("Fees have been updated with inflation.")
