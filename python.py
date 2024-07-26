import json
import speech_recognition as sr
from googletrans import Translator
from spellchecker import SpellChecker
import pyttsx3

# Initialize necessary components
recognizer = sr.Recognizer()
translator = Translator()
spell = SpellChecker()
engine = pyttsx3.init()

# Load medical vocabulary
def load_medical_vocabulary(filepath):
    with open(filepath, 'r') as file:
        medical_terms = file.read().splitlines()
    spell.word_frequency.load_words(medical_terms)
    return medical_terms

# Load dataset
def load_dataset(filepath):
    with open(filepath, 'r') as file:
        dataset = json.load(file)
    return dataset

# Autocorrect function
def autocorrect_text(text):
    corrected_words = []
    for word in text.split():
        if word.lower() in spell:
            corrected_words.append(word)
        else:
            corrected_words.append(spell.correction(word))
    corrected_text = ' '.join(corrected_words)
    return corrected_text

# Function to process symptoms
def process_symptoms(text, medical_terms):
    symptoms = [word for word in text.split() if word.lower() in medical_terms]
    return symptoms

# Function to find possible diseases
def find_possible_diseases(symptoms, dataset):
    possible_diseases = []
    for symptom in symptoms:
        if symptom in dataset["symptoms_to_diseases"]:
            possible_diseases.extend(dataset["symptoms_to_diseases"][symptom])
    return possible_diseases

# Function to recommend medicines
def recommend_medicines(diseases, dataset):
    recommended_medicines = []
    for disease in diseases:
        if disease in dataset["diseases_to_medicines"]:
            recommended_medicines.extend(dataset["diseases_to_medicines"][disease])
    return recommended_medicines

# Load medical vocabulary and dataset
medical_terms = load_medical_vocabulary('medical_vocabulary.txt')
dataset = load_dataset('medical_dataset.json')

# Main function
def main():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    print("Audio captured")
    
    try:
        print("Recognizing speech...")
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")
        
        print("Translating text...")
        translated_text = translator.translate(speech_text, src='en', dest='en').text
        print(f"Translated text: {translated_text}")
        
        print("Autocorrecting text...")
        corrected_text = autocorrect_text(translated_text)
        print(f"Corrected text: {corrected_text}")
        
        print("Processing text...")
        symptoms = process_symptoms(corrected_text, medical_terms)
        diseases = find_possible_diseases(symptoms, dataset)
        medicines = recommend_medicines(diseases, dataset)
        
        print(f"Extracted symptoms: {symptoms}")
        print(f"Possible diseases: {diseases}")
        print(f"Recommended medicines: {medicines}")
        
        response_text = f"Based on your symptoms, you might have {', '.join(diseases)}. You can take {', '.join(medicines)}."
        print(response_text)
        
        engine.say(response_text)
        engine.runAndWait()
        print("Response spoken")
    except Exception as e:
        print("Could not process the audio. Error:", str(e))

if __name__ == "__main__":
    main()
