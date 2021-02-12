import Levenshtein as lev

def leven(str1, str2):
    Distance = lev.distance(str1.lower(), str2.lower())
    Ratio = lev.ratio(str1.lower(), str2.lower())
#     print(Ratio)
    if Ratio > .95:
        return True
    else:
        return False

import re
def merge_awards(results):
    A = []
    B = []
    C = []
    for i in range(len(results)):
        if re.search("-",results[i][0]):
            A.append(results[i])
        else:
            B.append(results[i])
    # print(A)
    for a in A:
        str1 = a[0]
        has_merge = False
        for b in B:
            str2 = b[0]
            if leven(str1,str2):
                C.append((str1,a[1]+b[1]))
#                 print(str1,"  ",str2)
                B.remove(b)
                has_merge = True
        if not has_merge:
            C.append(a)          
    for b in B:
        C.append(b)
        
    return C

def filter_awards(results):
    awards = []
    for result in results:
        str1 = result[0]
        has_filter = False
        if awards:
            for award in awards:
                str2 = award[0]
                if leven(str1,str2):
                    has_filter = True
                    break
            if not has_filter:
                awards.append(result)
        else:
            awards.append(result)
    return awards

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

def str_handler(text):
    size = len(text)
    i = size - 1
    idx = size
    text = text.replace(",","-")
    
    while i >= 0:
        if text[i]<='z' and text[i]>='a':
            idx = i+1 
            break
        i -= 1
    return text[:idx].strip()       

def extract_award(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
#     filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filter_words = ['golden','globes', 'goldenglobe','globes', 'glodenglobes', 'http','2013','2015','2018','2019','2020']
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words and w not in filter_words:
#             w = w.replace('-',",")
            w = w.replace('/',",")
            filtered_sentence.append(w)
    result = ""
    start = False
#     print(filtered_sentence)
#     if re.search('best screenplay - motion picture',text):
#         print(text)
        
    for word in filtered_sentence:    
        if word == 'best':
            start = True
            result += word + " "
            continue
        
        if start and (re.match('w[io]n',word) or re.match('go(es)',word) or re.match('at',word) or re.match('went to',word) or re.match('[;\?:.!@#`]',word)):
            return str_handler(result.strip())

        if start:
            result += word+" "
    return str_handler(result.strip())
#     print(result)

def sanitize(lst):
    level0 = ['screenplay','director','foreign','motion','original','television','tv','animated','song']
    level1 = ['actor','actress']
    level2 = ['supporting','tv','television','motion','series']
    level3 = ['motion','tv','television','drama','comedy','musical']
    results = []
    for r in lst:
        text = r[0]
        if any([kw in text for kw in level1]):
            if any([kw2 in text for kw2 in level2]):
                l = []
                for kw2 in level2:
                    if kw2 in text:
                        l.append(kw2)
                        break
                if any([kw3 in text for kw3 in level3]):
                    for kw3 in level3:
                        if kw3 in text and kw3 not in l:
                            results.append(r)
                            break
                       
        else:
            if any([kw in text for kw in level0]):
                results.append(r)
    return results    
        
def final_sanitize(lst):
    level0 = ['screenplay','director','foreign','animated','song','original','motion','television','tv']
    level1 = ['actor','actress']
    level2 = ['supporting','tv','television','motion','series']
    level3 = ['motion','tv','television','drama','comedy','musical']
    results = []
    visited = set()
    for r in lst:
        text = r[0]
        key1 = ''
        key2 = ''
        key3 = ''
        if any([kw in text for kw in level1]):
            for kw in level1:    
                if kw in text:
                    key1 = kw
                    break
            if any([kw2 in text for kw2 in level2]):
                l = []
                for kw2 in level2:
                    if kw2 in text:
                        l.append(kw2)
                        key2 = kw2
                        break
                if any([kw3 in text for kw3 in level3]):
                    for kw3 in level3:
                        if kw3 in text and kw3 not in l:
                            key3 = kw3
                            key = key1+' '+key2+' '+ key3
                            if key not in visited:
                                visited.add(key)
                                results.append(r)
                            break
                       
        else:
            if any([kw in text for kw in level0]):
                l = []
                for kw in level0:
                    if kw in text:
                        if kw not in visited:
                            visited.add(kw)
                            results.append(r)
                        elif kw == "motion":
                            if 'drama' in text:
                                key = kw+' drama'
                                if key not in visited:
                                    visited.add(kw)
                                    results.append(r)
                            elif 'comedy' in text:
                                key = kw+' comedy'
                                if key not in visited:
                                    visited.add(kw)
                                    results.append(r)
                            
                        break
                
    return results 

import re
import regex
from collections import Counter
def get_allAwards(tweets,year):
    # reg = regex.Regex()
    search_terms = ['best','w[io]n','go(es)? to','went to',':']
    award_names = []
    for tweet in tweets:
        text = tweet['text'].lower()
        if 'RT' not in tweet['text']:
            if re.search(search_terms[0],text) and (re.search(search_terms[1],text) or re.search(search_terms[2],text) or re.search(search_terms[3],text) or re.search(search_terms[4],text)):
                extract_str = extract_award(text)
                if re.search('usa',extract_str):
                    continue
                if re.search('globe',extract_str):
                    continue
                if len(extract_str.split())<4:
                    continue
                count = Counter(extract_str)
                if count['-']>1:
                    continue
                award_names.append(extract_str)
    results = Counter(award_names).most_common()   

    results = merge_awards(results[:200])
    # results = Counter(results).most_common() 
    results = sorted(results, key = lambda x: x[1],reverse = True)
    results = filter_awards(results)
    results = sanitize(results[:100])
    results = final_sanitize(results)
    answers = []
    for i in range(len(results)):
        if i>=26:
            break
        res = results[i]
        answers.append(res[0])
    return answers

# import json
# tweets = json.load(open("gg2015.json"))
# results = get_allAwards(tweets,2015)
# print(results)