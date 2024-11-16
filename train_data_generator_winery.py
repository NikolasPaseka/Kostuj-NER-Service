import json
import random
import pandas as pd

# Function to get data from the Excel file
def get_data_from_excel():
    file_path = 'data/kost2023.xlsx'
    sheet_name = 'vinařství'  # Replace with your actual sheet name
    columns_to_read = ['vinařství', 'obec', 'e-mail', 'telefon', 'web']
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_data[columns_to_read]

# Function to generate a random sentence
def generate_sentence(winery, address, email, phone, web):
    vocabulary = {
        "winery": ["vinařství", "vinař", "název", "jméno"],
        "address": ["obec", "adresa", "město"],
        "email": ["e-mail", "email", "emailová adresa"],
        "phone": ["telefon", "mobil", "telefonní číslo"],
        "web": ["web", "adresa", "webová stránka", ""]
    }

    sentence_parts = [
        f"{random.choice(vocabulary['winery'])} {winery}",
        f"{random.choice(vocabulary['address'])} {address}",
        f"{random.choice(vocabulary['email'])} {email}",
        f"{random.choice(vocabulary['phone'])} {phone}",
        f"{random.choice(vocabulary['web'])} {web}"
    ]
    random.shuffle(sentence_parts)
    random_sentence = " ".join(sentence_parts).replace("  ", " ").strip()
    return random_sentence

# Function to tag entities in a sentence
def tag_entities(sentence, winery, address, email, phone, web):
    entities = []
    entities.append([sentence.index(winery), sentence.index(winery) + len(winery), "VINAŘSTVÍ"])
    entities.append([sentence.index(address), sentence.index(address) + len(address), "OBEC"])
    entities.append([sentence.index(str(email)), sentence.index(str(email)) + len(str(email)), "E-MAIL"])
    entities.append([sentence.index(str(phone)), sentence.index(str(phone)) + len(str(phone)), "TELEFON"])
    entities.append([sentence.index(str(web)), sentence.index(str(web)) + len(str(web)), "WEB"])
    return entities

data = get_data_from_excel()

dataMap = {
    "wineries": data["vinařství"].dropna().tolist(),
    "address": data["obec"].dropna().tolist(),
    "email": data["e-mail"].dropna().tolist(),
    "phone": data["telefon"].dropna().tolist(),
    "web": data["web"].dropna().tolist()
}

# Create the JSON structure
ner_data = {"classes": ["VINAŘSTVÍ", "OBEC", "E-MAIL", "TELEFON", "WEB"], "annotations": []}

sentences = []
for _ in range(200):
    winery = random.choice(dataMap["wineries"])
    address = random.choice(dataMap["address"])
    email = random.choice(dataMap["email"])
    phone = random.choice(dataMap["phone"])
    web = random.choice(dataMap["web"])

    try:
        phone = int(phone)
    except ValueError:
        phone = 555555555

    sentence = generate_sentence(winery, address, email, phone, web)
    entities = tag_entities(sentence, winery, address, email, phone, web)
    sentences.append(sentence)
    ner_data["annotations"].append([sentence, {"entities": entities}])

# Print the generated sentences
with open('generated_train_data/winery_sentences.txt', 'w', encoding='utf-8') as file:
    for sentence in sentences:
        file.write(sentence + '\n')

# Save the JSON data to a file
with open('generated_train_data/winery_ner_tagged_sentences.json', 'w', encoding='utf-8') as file:
    json.dump(ner_data, file, ensure_ascii=False, indent=4)