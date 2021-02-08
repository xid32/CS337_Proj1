import nltk
import json
import re
from get_presenters_utils import *


def get_presenters_results(awards, year):
    # TODO: choose scripts
    scripts = AWARD_SCRIPTS

    # Open Corresponding Year Json File:
    f = open('files/gg%s.json' % year)
    data = json.load(f) 

    # Get names dictionary from Corresponding Year Json File:
    print("Getting Names: ")
    names = get_names(year)

    # Output Json File
    result = {"Hosts": []}
    
    for award in awards:
        result[award] = {"Presenters":[], "Nominees":[], "Winners":[]}

    print("Extracting presenters: ")
    # Iterate to Extract Information
    for award in awards:
        for i in range(0, len(data)):
            # if i % 100 == 0: print(i)
            text = data[i]["text"].lower()
            keyWords = scripts[award]
            if isContainAll(text, keyWords):
                for key in names:
                    name_normalized = remove_punc(key).lower()
                    if name_normalized in text:
                        names[key] += 20
                    if isContainName(text, name_normalized):
                        names[key] += 1

        new_dict = get_dict_larger_than(names, 1)
        my_answer = sorted(new_dict, key=new_dict.get, reverse=True)[:2]
        result[award]["Presenters"] = my_answer

        # Place Holders
        result[award]["Winners"] = []
        result[award]["Nominees"] = []

        # Print Result
        print("Award: ", award)
        print("     my   answers: ,", my_answer)
        # print("     true answers: ", *answer_dict[award], sep = ", ")
        print("\n")
        names = dict.fromkeys(names, 0)
    with open('gg%sresults.json' % year, 'w', encoding='utf8') as outfile:
        json.dump(result, outfile)