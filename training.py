from collections import Counter
import nltk

with open('actual_both_dialogues.txt', 'r', encoding='utf8') as doc:
    text = []
    for line in doc.readlines():
        try:
            speaker, dialogue = line.split(': ', 1)
            dialogue = nltk.word_tokenize(dialogue.lower())
            text.append(speaker.lower()+":") 
            text += dialogue
        except ValueError:
            print(line)


# text = text.lower()
# text_tokenized = nltk.word_tokenize(text)

token_to_int = dict(Counter(text_tokenized))
