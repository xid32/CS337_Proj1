import nltk
import json
import re
from textblob import TextBlob
# TODO: get_hosts()

def get_sentiment_words(sent, dict, exclude_words):
    targets = ["JJ"]
    words = nltk.word_tokenize(sent)
    tags = nltk.pos_tag(words)
    words_list = list(filter(lambda x: x[1] in targets, tags))
    for word_tuple in words_list:
        word = word_tuple[0]
        if word in exclude_words: continue
        if len(word) <= 2: continue
        if word in dict:
            dict[word] += 1
        else:
            dict[word] = 0

def get_sentiments(hosts, year):
    exclude_words = ["golden", "globes", "@", "goldenglobes", "best"]
    for name in hosts:
        name_token = nltk.word_tokenize(name)
        for token in name_token:
            exclude_words.append(token)

    f = open('files/gg%s.json' % year)
    data = json.load(f) 
    sentiments_dict = {}
    for host in hosts:
        polarity_sum = 0
        polarity_count = 0
        word_dict = {}
        for i in range(0, len(data)):
            text = data[i]["text"].lower()
            if host in text:
                blob = TextBlob(text)
                for i in range(0, len(blob.sentences)):
                    if blob.sentences[i].polarity != 0:
                        polarity_sum += blob.sentences[i].polarity
                        polarity_count += 1

                        get_sentiment_words(str(blob.sentences[i]), word_dict, exclude_words)
        final_word_dict = sorted(word_dict, key=word_dict.get, reverse=True)[:5]


        sentiments_dict[host] = {}
        sentiments_dict[host]["ave_score"] = polarity_sum / (polarity_count + 1)
        sentiments_dict[host]["words"] = final_word_dict
    return sentiments_dict
                

   