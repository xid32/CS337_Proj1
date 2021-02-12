import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.tokenize import word_tokenize 
import re
import imdb
import Levenshtein as lev
import json
import regex
from collections import Counter

def leven(str1, str2):
    Distance = lev.distance(str1.lower(), str2.lower())
    Ratio = lev.ratio(str1.lower(), str2.lower())
#     print(Ratio)
    if Ratio > .95:
        return True
    else:
        return False
    

def validate_name(name):
    ia = imdb.IMDb()
    people = ia.search_person(name)
    for p in people:
        str1 = p['name']
        str2 = name
        if leven(str1,str2):
            return True
    return False

def extract_str(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)    
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    result = ""
#     print(filtered_sentence)
    str1 = ""
    str2 = ""
    for i in range(len(filtered_sentence)):
        if re.match('host.*',filtered_sentence[i]):
            if i<4:
                continue
            str1 = filtered_sentence[i-2]+" "+filtered_sentence[i-1]
            str2 = filtered_sentence[i-4]+" "+filtered_sentence[i-3]
            return str1,str2
    return str1,str2

def get_hosts(tweets):
    search_term = 'host'
    results=[]
    for tweet in tweets:
        text = tweet['text'].lower()
    #     print(text)
        if 'RT' not in tweet['text']:
            if re.search(search_term,text) and re.search('and',text):
    #             print(text)
                name1,name2 = extract_str(text)
                if len(name1)==0:
                    continue
                else:
                    results.append((name1,name2))
                    
    results = Counter(results).most_common()            
    for res in results:
        name1 = res[0][0]
        name2 = res[0][1]
        if validate_name(name1) and validate_name(name2):
            # print(name1," ",name2)
            return [name1,name2]

# tweets = json.load(open("gg2013.json"))
# result = get_hosts(tweets)
# print(result[0])
# print(result[1])
            

