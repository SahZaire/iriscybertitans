import spacy
import random
import json
import requests
import nltk  # Make sure to install nltk and download WordNet
from nltk.corpus import wordnet as wn

def generate_questions_pipeline(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    questions = []

    # POS Tagging
    for token in doc:
        if token.pos_ == "PROPN":
            if "PERSON" in [ent.label_ for ent in doc.ents]:
                questions.append(f"Who is {token.text}? How is {token.text} related to the topic?")
            else:
                questions.append(f"What is {token.text}? Can you explain how {token.text} works?")
        elif token.pos_ == "NOUN":
            questions.append(f"What is {token.text}? Can you explain how {token.text} works?")
        elif token.pos_ == "VERB":
            questions.append(f"What does {token.text} mean?")
        elif token.pos_ == "ADV":
            questions.append(f"How does the action happen in the sentence? Use the adverb '{token.text}' to explain.")
        elif token.pos_ == "ADJ":
            questions.append(f"Describe the {token.head.text} using the adjective '{token.text}'.")

    # Named Entity Recognition (NER)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            questions.append(f"Who is {ent.text}?")
        elif ent.label_ == "ORG":
            questions.append(f"What is {ent.text}?")
        elif ent.label_ == "GPE":
            questions.append(f"What is located in {ent.text}?")

    return questions

def generate_questions_for_paragraph(paragraph):
    nlp = spacy.load("en_core_web_sm")
    sentences = [sent.text for sent in nlp(paragraph).sents]
    questions = {}
    for sentence in sentences:
        questions[sentence] = generate_questions_pipeline(sentence)
    return questions

def genQueFunc2(paragraph):
    questions_dict = generate_questions_for_paragraph(paragraph)
    for sentence, sentence_questions in questions_dict.items():
        questions_dict[sentence] = sentence_questions

    return json.dumps(questions_dict, indent=4)

finalDict = {}
def fetch_answer(question):
    url = 'http://127.0.0.1:8080/qna'
    data = {'question': question, 'context': paragraph}
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    data = response.json()
    answer = data  # Assuming the answer is in the 'answer' key
    finalDict[question] = answer

# Example usage:
paragraph = '''
    The Sahara Desert, spanning approximately 3.6 million square miles, is the world's largest hot desert. While often associated with vast stretches of sand dunes, the Sahara's landscape is diverse, featuring rocky plateaus, mountains, and occasional vegetation. Surprisingly, Antarctica, primarily known for its icy expanses, is the driest and windiest continent on Earth. With an average precipitation of merely 2 inches per year, it is technically classified as a desert. Moving to technological achievements, the International Space Station (ISS) orbits the Earth at an average speed of about 28,000 kilometers per hour, allowing it to complete one orbit roughly every 90 minutes. This remarkable spacecraft serves as a microgravity and space environment research laboratory, hosting scientific experiments from countries around the world. In the realm of biodiversity, the Amazon Rainforest is home to an astonishing array of plant and animal species, with estimates suggesting that it houses about 390 billion individual trees representing over 16,000 different species. These facts highlight the incredible diversity and fascinating characteristics found within some of the Earth's most iconic natural and technological features.
'''

set1_json = genQueFunc2(paragraph)
set1 = json.loads(set1_json)
selected_questions = []
for sentence, questions in set1.items():
    selected_questions.extend(questions[:3])

for question in selected_questions:
    fetch_answer(question)  # Call fetch_answer for each question

# Print the final dictionary with questions and answers
print(finalDict)

