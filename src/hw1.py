import nltk
import json
f = open('files/gg2013.json')
data = json.load(f)

for i in range(0, 5):
    text = nltk.word_tokenize(data[i]["text"])
    print(nltk.pos_tag(text))