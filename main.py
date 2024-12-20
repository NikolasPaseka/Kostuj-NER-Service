from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy

# Load the trained SpaCy model (replace 'en_core_web_sm' with your model's name)
nlp_wine = spacy.load("models/wine_ner_model")
nlp_winery = spacy.load("models/winery_ner_model")

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a request body schema
class SentenceRequest(BaseModel):
    sentence: str

# Define the response model
class EntityResponse(BaseModel):
    winery: str = None
    wine: str = None
    year: str = None
    color: str = None
    rating: str = None
    ratingCommission: str = None
    resultSweetness: str = None

class WineryResponse(BaseModel):
    name: str = None
    address: str = None
    email: str = None
    phoneNumber: str = None
    websitesUrl: str = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define an endpoint for NER
@app.post("/ner/")
async def extract_entities(request: SentenceRequest):
    # Process the sentence using the SpaCy model
    doc = nlp_wine(request.sentence.lower())
    
    # Extract entities and their labels
    # entities = []
    # for ent in doc.ents:
    #     entities.append({"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char})

       # Initialize an empty response object
    responseObject = EntityResponse()
    
    color_switch = {
        "červená": "red",
        "červené": "red",
        "bílá": "white",
        "bílé": "white",
        "růžová": "rose",
        "růžové": "rose",
        "rose": "rose",
        "rosé": "rose",
    }
    result_sweetness_switch = {
        "suché": "dry",
        "polosuché": "off-dry",
        "polosladké": "semi-sweet",
        "sladké": "sweet",
    }

    # Extract entities and assign them to the corresponding fields
    for ent in doc.ents:
        if ent.label_ == "VINAŘSTVÍ":
            responseObject.winery = ent.text
        elif ent.label_ == "VÍNO":
            responseObject.wine = ent.text
        elif ent.label_ == "ROČNÍK":
            responseObject.year = ent.text
        elif ent.label_ == "BARVA":
            responseObject.color = color_switch.get(ent.text.lower(), ent.text)
        elif ent.label_ == "HODNOCENÍ":
            responseObject.rating = ent.text
        elif ent.label_ == "KOMISE":
            responseObject.ratingCommission = ent.text
        elif ent.label_ == "SLADKOST":
            responseObject.resultSweetness = result_sweetness_switch.get(ent.text.lower(), None)
    
    # Return the extracted entities
    #return {"sentence": request.sentence, "entities": entities}
    return {"sentence": request.sentence, "entity": responseObject}

@app.post("/ner/winery")
async def extract_entities(request: SentenceRequest):
    # Process the sentence using the SpaCy model
    doc = nlp_winery(request.sentence)

    # Initialize an empty response object
    responseObject = WineryResponse()
    
    # Extract entities and assign them to the corresponding fields
    for ent in doc.ents:
        if ent.label_ == "VINAŘSTVÍ":
            responseObject.name = ent.text
        elif ent.label_ == "OBEC":
            responseObject.address = ent.text
        elif ent.label_ == "E-MAIL":
            responseObject.email = ent.text
        elif ent.label_ == "TELEFON":
            responseObject.phoneNumber = ent.text
        elif ent.label_ == "WEB":
            responseObject.websitesUrl = ent.text

    return {"sentence": request.sentence, "entity": responseObject}

# Run with: uvicorn main:app --reload
