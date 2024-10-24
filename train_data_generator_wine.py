import json
import random
import pandas as pd

# Function to get data from the Excel file
def get_data_from_excel():
    file_path = 'data/kost2023.xlsx'
    sheet_name = 'vína'  # Replace with your actual sheet name
    columns_to_read = ['vinařství', 'odruda', 'barva', 'ročník', 'Body']
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_data[columns_to_read]

# Function to generate a random sentence
def generate_sentence(winery, wine, color, year, rating):
    vocabulary = {
        "winery": ["vinařství", "vinař"],
        "year": ["ročník", "rok", "ročníku"],
        "hodnocení": ["body", "hodnocení"],
        "wine": ["víno", "vino", "odrůda"],
        "color": ["barva", "barvy", ""]
    }

    sentence_parts = [
        f"{random.choice(vocabulary['winery'])} {winery}",
        f"{random.choice(vocabulary['wine'])} {wine}",
        f"{random.choice(vocabulary['color'])} {color}",
        f"{random.choice(vocabulary['year'])} {year}",
        f"{random.choice(vocabulary['hodnocení'])} {rating}"
    ]
    random.shuffle(sentence_parts)
    random_sentence = " ".join(sentence_parts).replace("  ", " ").strip()
    return random_sentence

# Function to tag entities in a sentence
def tag_entities(sentence, winery, wine, color, year, rating):
    entities = []
    entities.append([sentence.index(winery), sentence.index(winery) + len(winery), "VINAŘSTVÍ"])
    entities.append([sentence.index(color), sentence.index(color) + len(color), "BARVA"])
    entities.append([sentence.index(wine), sentence.index(wine) + len(wine), "VÍNO"])
    entities.append([sentence.index(str(year)), sentence.index(str(year)) + len(str(year)), "ROČNÍK"])
    entities.append([sentence.index(str(rating)), sentence.index(str(rating)) + len(str(rating)), "HODNOCENÍ"])
    return entities

data = get_data_from_excel()

dataMap = {
    "wineries": data["vinařství"],
    "wines": data["odruda"],
    "colors": ["bílá", "červená", "růžová"],
    "years": data["ročník"],
    "ratings": data["Body"]
}

# Create the JSON structure
ner_data = {"classes": ["VINAŘSTVÍ", "BARVA", "ROČNÍK", "HODNOCENÍ", "VÍNO"], "annotations": []}

sentences = []
for _ in range(2000):
    winery = random.choice(dataMap["wineries"])
    wine = random.choice(dataMap["wines"])
    color = random.choice(dataMap["colors"])
    year = random.choice(dataMap["years"])
    rating = random.choice(dataMap["ratings"])

    try:
        year = int(year)
    except ValueError:
        year = 2022  # Default value if conversion fails

    sentence = generate_sentence(winery, wine, color, year, rating)
    entities = tag_entities(sentence, winery, wine, color, year, rating)
    sentences.append(sentence)
    ner_data["annotations"].append([sentence, {"entities": entities}])

# Print the generated sentences
with open('generated_train_data/generated_sentences.txt', 'w', encoding='utf-8') as file:
    for sentence in sentences:
        file.write(sentence + '\n')

# Save the JSON data to a file
with open('generated_train_data/ner_tagged_sentences.json', 'w', encoding='utf-8') as file:
    json.dump(ner_data, file, ensure_ascii=False, indent=4)