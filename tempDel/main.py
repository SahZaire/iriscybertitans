import spacy
from nltk.corpus import wordnet as wn
import random
import json

def get_similar_words(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def generate_questions_pipeline(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    questions = {
        "Dependency_Parsing": [],
        "POS_Tagging": [],
        "NER": []
    }

    # Dependency Parsing
    root = [token.text for token in doc if token.dep_ == "ROOT"]
    dependency_question = f"What does '{root[0]}' mean?" if root else "What is the main idea of the sentence?"
    questions["Dependency_Parsing"].append(dependency_question)

    # POS Tagging
    for token in doc:
        if token.pos_ == "PROPN":
            if "PERSON" in [ent.label_ for ent in doc.ents]:
                questions["POS_Tagging"].append(f"Who is {token.text}? How is {token.text} related to the topic?")
            else:
                questions["POS_Tagging"].append(f"What is {token.text}? Can you explain how {token.text} works?")
        elif token.pos_ == "NOUN":
            questions["POS_Tagging"].append(f"What is {token.text}? Can you explain how {token.text} works?")
        elif token.pos_ == "VERB":
            questions["POS_Tagging"].append(f"What does {token.text} mean?")
        elif token.pos_ == "ADV":
            questions["POS_Tagging"].append(f"How does the action happen in the sentence? Use the adverb '{token.text}' to explain.")
        elif token.pos_ == "ADJ":
            questions["POS_Tagging"].append(f"Describe the {token.head.text} using the adjective '{token.text}'.")

    # Named Entity Recognition (NER)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            questions["NER"].append(f"Who is {ent.text}?")
        elif ent.label_ == "ORG":
            questions["NER"].append(f"What is {ent.text}?")
        elif ent.label_ == "GPE":
            questions["NER"].append(f"What is located in {ent.text}?")

    return questions

def generate_questions_for_paragraph(paragraph):
    nlp = spacy.load("en_core_web_sm")
    sentences = [sent.text for sent in nlp(paragraph).sents]
    questions = {}
    for sentence in sentences:
        questions[sentence] = generate_questions_pipeline(sentence)
    return questions

def genQueFunc(paragraph):
    questions_dict = generate_questions_for_paragraph(paragraph)
    for sentence, category_questions in questions_dict.items():
        sentence_questions = []
        for category, category_questions in category_questions.items():
            question_options = []
            for question in category_questions:
                similar_options = get_similar_words(question.split()[-1])
                random.shuffle(similar_options)
                question_options.append({ "question": question, "options": similar_options[:3] })
            sentence_questions.append({ category: question_options })
        questions_dict[sentence] = sentence_questions

    return json.dumps(questions_dict, indent=4)

# Example usage:
paragraph = '''
    The Sahara Desert, spanning approximately 3.6 million square miles, is the world's largest hot desert. While often associated with vast stretches of sand dunes, the Sahara's landscape is diverse, featuring rocky plateaus, mountains, and occasional vegetation. Surprisingly, Antarctica, primarily known for its icy expanses, is the driest and windiest continent on Earth. With an average precipitation of merely 2 inches per year, it is technically classified as a desert. Moving to technological achievements, the International Space Station (ISS) orbits the Earth at an average speed of about 28,000 kilometers per hour, allowing it to complete one orbit roughly every 90 minutes. This remarkable spacecraft serves as a microgravity and space environment research laboratory, hosting scientific experiments from countries around the world. In the realm of biodiversity, the Amazon Rainforest is home to an astonishing array of plant and animal species, with estimates suggesting that it houses about 390 billion individual trees representing over 16,000 different species. These facts highlight the incredible diversity and fascinating characteristics found within some of the Earth's most iconic natural and technological features.
'''

print(genQueFunc(paragraph))
