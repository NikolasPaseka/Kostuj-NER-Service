import json
import random
import pandas as pd

# Function to get data from the Excel file
def get_data_from_excel():
    file_path = 'data/kost2023.xlsx'
    sheet_name = 'vína'  # Replace with your actual sheet name
    columns_to_read = ['vinařství', 'odruda', 'barva', 'ročník', 'Body', 'komise']
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_data[columns_to_read]

# Function to generate a random sentence
def generate_sentence(winery, wine, color, year, rating, ratingCommission, resultSweetness):
    vocabulary = {
        "winery": ["vinařství", "vinař"],
        "year": ["ročník", "rok", "ročníku"],
        "hodnocení": ["body", "hodnocení"],
        "wine": ["víno", "odrůda"],
        "color": ["barva", "barvy", ""],
        "ratingCommission": ["komise"],
        "resultSweetness": ["sladkost", ""]
    }

    sentence_parts = [
        f"{random.choice(vocabulary['winery'])} {winery}",
        f"{random.choice(vocabulary['wine'])} {wine}",
        f"{random.choice(vocabulary['color'])} {color}",
        f"{random.choice(vocabulary['year'])} {year}",
        f"{random.choice(vocabulary['hodnocení'])} {rating}",
        # f"{random.choice(vocabulary['ratingCommission'])} {ratingCommission}",
        f"{random.choice(vocabulary['resultSweetness'])} {resultSweetness}",
    ]
    random.shuffle(sentence_parts)
    random_sentence = " ".join(sentence_parts).replace("  ", " ").strip()
    return random_sentence

# Function to tag entities in a sentence
def tag_entities(sentence, winery, wine, color, year, rating, ratingCommission, resultSweetness):
    entities = []
    entity_positions = [
        (sentence.index(winery), sentence.index(winery) + len(winery), "VINAŘSTVÍ"),
        (sentence.index(color), sentence.index(color) + len(color), "BARVA"),
        (sentence.index(wine), sentence.index(wine) + len(wine), "VÍNO"),
        (sentence.index(str(year)), sentence.index(str(year)) + len(str(year)), "ROČNÍK"),
        (sentence.index(str(rating)), sentence.index(str(rating)) + len(str(rating)), "HODNOCENÍ"),
        (sentence.index(resultSweetness), sentence.index(resultSweetness) + len(resultSweetness), "SLADKOST")
    ]
    
    entity_positions.sort(key=lambda x: x[0])
    
    for start, end, label in entity_positions:
        if not entities or start > entities[-1][1]:
            entities.append([start, end, label])
    
    return entities

data = get_data_from_excel()

dataMap = {
    "wineries": data["vinařství"],
    "wines": data["odruda"],
    "colors": ["bílá", "bílé", "červené", "červená", "růžová", "růžové", "rosé"],
    "years": data["ročník"],
    "ratings": data["Body"],
    "ratingCommision": data["komise"],
    "resultSweetness": ["suché", "polosuché", "polosladké", "sladké"]
}

# Create the JSON structure
ner_data = {"classes": ["VINAŘSTVÍ", "BARVA", "ROČNÍK", "HODNOCENÍ", "VÍNO", "SLADKOST"], "annotations": []}

sentences = []
for _ in range(2000):
    winery = random.choice(dataMap["wineries"])
    wine = random.choice(dataMap["wines"])
    color = random.choice(dataMap["colors"])
    year = random.choice(dataMap["years"])
    rating = random.choice(dataMap["ratings"])
    ratingCommission = random.choice(dataMap["ratingCommision"])
    resultSweetness = random.choice(dataMap["resultSweetness"])

    try:
        year = int(year)
    except ValueError:
        year = 2022  # Default value if conversion fails

    sentence = generate_sentence(winery, wine, color, year, rating, ratingCommission, resultSweetness)
    entities = tag_entities(sentence, winery, wine, color, year, rating, ratingCommission, resultSweetness)
    sentences.append(sentence)
    ner_data["annotations"].append([sentence, {"entities": entities}])

# Print the generated sentences
with open('generated_train_data/generated_sentences.txt', 'w', encoding='utf-8') as file:
    for sentence in sentences:
        file.write(sentence.lower() + '\n')

# Save the JSON data to a file
with open('generated_train_data/ner_tagged_sentences.json', 'w', encoding='utf-8') as file:
    json.dump(ner_data, file, ensure_ascii=False, indent=4)