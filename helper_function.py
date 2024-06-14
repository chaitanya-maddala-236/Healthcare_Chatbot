import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer

with open("data/healthcare_data.json", "r") as file:
    healthcare_data = json.load(file)

symptom_to_disease = healthcare_data.get("symptom_to_disease", {})

def get_random_disease(symptom):
    possible_diseases = symptom_to_disease.get(symptom, [])
    return random.choice(possible_diseases) if possible_diseases else "Unknown"

symptoms = list(symptom_to_disease.keys())
vectorizer = TfidfVectorizer()
symptom_vectors = vectorizer.fit_transform(symptoms)
