import csv


# ---- AI-generated (Claude), see ai_transcript_helper.md ----
def convert(value):
    value = value.strip()
    if value == '':
        return None
    if len(value) > 1 and value[0] == '0' and value[1] != '.':
        return value
    try:
        return int(value)
    except ValueError:
        pass
    try:
        result = float(value)
        if result != result or result in (float('inf'), float('-inf')):
            return value
        return result
    except ValueError:
        return value


def data_cleaner(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        data_cleaned = []
        for row in reader:
            # skip blank lines
            if not any(cell.strip() for cell in row):
                continue
            data_cleaned.append(tuple(convert(cell) for cell in row))
    return data_cleaned
# ---- end AI-generated ----


def get_choice(lst):
    choice = input("Enter choice number: ").strip()
    while not choice.isdigit() or int(choice) not in lst:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ").strip()
    return int(choice)


def get_text(prompt):
    text = input(prompt).strip()
    while text == "":
        print("This field can't be empty. Try again")
        text = input(prompt).strip()
    return text
