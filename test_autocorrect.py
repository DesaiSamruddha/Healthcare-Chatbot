from spellchecker import SpellChecker

# Load medical vocabulary
def load_medical_vocabulary(filepath):
    with open(filepath, 'r') as file:
        medical_terms = file.read().splitlines()
    return medical_terms

# Initialize spellchecker with medical vocabulary
def initialize_spellchecker(medical_terms):
    spell = SpellChecker()
    spell.word_frequency.load_words(medical_terms)
    return spell

# Autocorrect function
def autocorrect_text(text, spell):
    corrected_words = []
    for word in text.split():
        if word.lower() in spell:
            corrected_words.append(word)
        else:
            corrected_words.append(spell.correction(word))
    corrected_text = ' '.join(corrected_words)
    return corrected_text

# Main function to test autocorrect
def main():
    # Call load_medical_vocabulary with the path to your medical vocabulary file
    medical_vocabulary = load_medical_vocabulary('medical_vocabulary.txt')
    spellchecker = initialize_spellchecker(medical_vocabulary)
    
    test_sentences = [
        "I have a fever",
        "I am feeling hadache",
        "I have a cugh and cold",
        "I think I have diabees",
        "I am experiencing hypertesion",
        "I have asthma symptoms",
        "I might have strepthroat"
    ]
    
    for sentence in test_sentences:
        corrected_sentence = autocorrect_text(sentence, spellchecker)
        print(f"Original: {sentence}")
        print(f"Corrected: {corrected_sentence}")
        print("")

if __name__ == "__main__":
    main()



 
 timeout=5, phrase_time_limit=10