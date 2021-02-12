import nltk
import json
import re
from string import punctuation


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 
                   'best motion picture - drama', 
                   'best performance by an actress in a motion picture - drama', 
                   'best performance by an actor in a motion picture - drama', 
                   'best motion picture - comedy or musical', 
                   'best performance by an actress in a motion picture - comedy or musical', 
                   'best performance by an actor in a motion picture - comedy or musical', 
                   'best animated feature film', 
                   'best foreign language film', 
                   'best performance by an actress in a supporting role in a motion picture', 
                   'best performance by an actor in a supporting role in a motion picture', 
                   'best director - motion picture', 
                   'best screenplay - motion picture', 
                   'best original score - motion picture', 
                   'best original song - motion picture', 
                   'best television series - drama', 
                   'best performance by an actress in a television series - drama', 
                   'best performance by an actor in a television series - drama', 
                   'best television series - comedy or musical', 
                   'best performance by an actress in a television series - comedy or musical', 
                   'best performance by an actor in a television series - comedy or musical', 
                   'best mini-series or motion picture made for television', 
                   'best performance by an actress in a mini-series or motion picture made for television', 
                   'best performance by an actor in a mini-series or motion picture made for television', 
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 
                        'best motion picture - musical or comedy', 
                        'best performance by an actress in a motion picture - drama', 
                        'best performance by an actor in a motion picture - drama', 
                        'best performance by an actress in a motion picture - musical or comedy', 
                        'best performance by an actor in a motion picture - musical or comedy', 
                        'best performance by an actress in a supporting role in any motion picture', 
                        'best performance by an actor in a supporting role in any motion picture', 
                        'best director - motion picture', 'best screenplay - motion picture', 
                        'best motion picture - animated', 'best motion picture - foreign language', 
                        'best original score - motion picture', 'best original song - motion picture', 
                        'best television series - drama', 'best television series - musical or comedy', 
                        'best television limited series or motion picture made for television', 
                        'best performance by an actress in a limited series or a motion picture made for television', 
                        'best performance by an actor in a limited series or a motion picture made for television', 
                        'best performance by an actress in a television series - drama', 
                        'best performance by an actor in a television series - drama', 
                        'best performance by an actress in a television series - musical or comedy', 
                        'best performance by an actor in a television series - musical or comedy', 
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 
                        'cecil b. demille award']


stopWords = ["zero", "two", "president", "one", "movie","foreign", "present", "presents", "presented", "presenter", "presenters", "presenting", "award", "golden", "globes", "globe", "miu", "best", "supporting", "director",
             "motion", "picture", "original", "comedy", "musical","i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", 
             "your", "yours", "yourself", "yourselves", "he", "him", "his", 
             "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
             "they", "them", "their", "theirs", "themselves", "what", "which", 
             "who", "whom", "legends", "since", "legend", "this", "that", "fifty", "these", "those", "am", "is", "are", 
             "was", "were", "be", "video", "music", "been", "being", "shade", "have", "has", "had", "having", 
             "do", "does", "los", "represent", "red", "latinas", "did", "doing", "purple", "presented","a", "an", "the", "and", "but", "if", 
             "or", "because", "as", "until", "while", "of", "at", "by", "for", 
             "with", "about", "against", "representation", "between", "into", "through", "during", 
             "before", "after", "above", "ever", "say", "said", "below", "to", "from", "up", "down", "in", 
             "out", "on", "off", "show", "today", "carpet", "over", "under", "again", "further", "then", "once", 
             "here", "there", "when", "where", "why", "see", "solo", "how", "all", "any", "both", 
             "each", "few", "com", "more", "most", "other", "some", "such", "no", "nor", "not", 
             "only", "own", "same", "so", "sense", "than", "ver", "maggie", "downtown", "una", "mychael", "mejor", "series", "actress", "pres", "too", "very", "s", "t", "can", "will", 
             "just", "don", "should", "now", "actor", "film", "language", "miniseries","mini",
             "tv","miniserie", "serie", "party", "association", "press", "downton", "gina", "wins", "ad", "present", "night", "est", "legend","comedic", "gold", "goldenglobes", "goldenglobe"]

AWARD_SCRIPTS_1315 = {'cecil b. demille award': ["cecil", "demille"],
                 'best motion picture - drama': ['motion', 'drama'],
                 'best performance by an actress in a motion picture - drama': ["actress", "motion", "drama"],
                 'best performance by an actor in a motion picture - drama': ["actor", "motion", "drama"],
                 'best motion picture - comedy or musical': ["motion", "comedy", "musical"],
                 'best performance by an actress in a motion picture - comedy or musical': ["actress", "comedy", "musical"],
                 'best performance by an actor in a motion picture - comedy or musical': ["actor", "comedy", "musical"],
                 'best animated feature film': ["animated"],
                 'best foreign language film': ["foreign language"],
                 'best performance by an actress in a supporting role in a motion picture': ["actress", "supporting", "motion"],
                 'best performance by an actor in a supporting role in a motion picture': ["actor", "supporting", "motion"],
                 'best director - motion picture': ["director"],
                 'best screenplay - motion picture': ["screenplay", "motion"],
                 'best original score - motion picture': ["score", "motion"],
                 'best original song - motion picture': ["score", "motion"],
                 'best television series - drama': ["tv", "drama"],
                 'best performance by an actress in a television series - drama': ["actress", "tv", "drama"],
                 'best performance by an actor in a television series - drama':["actor", "tv", "drama"], 
                 'best television series - comedy or musical': ["tv", "comedy", "musical"],
                 'best performance by an actress in a television series - comedy or musical': ["actress", "tv", "comedy", "musical"],
                 'best performance by an actor in a television series - comedy or musical': ["actor", "tv", "comedy", "musical"],
                 'best mini-series or motion picture made for television': ["mini"],
                 'best performance by an actress in a mini-series or motion picture made for television': ["actress", "mini"],
                 'best performance by an actor in a mini-series or motion picture made for television': ["actor", "mini"],
                 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ["actress", "supporting", "mini"],
                 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ["actor", "supporting", "mini"]}


AWARD_SCRIPTS_1819 = {'cecil b. demille award': ["cecil", "demille"],
                 'best motion picture - drama': ['motion', 'drama'],
                 'best performance by an actress in a motion picture - drama': ["actress", "motion", "drama"],
                 'best performance by an actor in a motion picture - drama': ["actor", "motion", "drama"],
                 'best motion picture - musical or comedy': ["motion", "comedy", "musical"],
                 'best performance by an actress in a motion picture - musical or comedy': ["actress", "comedy", "musical"],
                 'best performance by an actor in a motion picture - musical or comedy': ["actor", "comedy", "musical"],
                 'best animated feature film': ["animated"],
                 'best foreign language film': ["foreign language"],
                 'best performance by an actress in a supporting role in a motion picture': ["actress", "supporting", "motion"],
                 'best performance by an actor in a supporting role in a motion picture': ["actor", "supporting", "motion"],
                 'best director - motion picture': ["director"],
                 'best screenplay - motion picture': ["screenplay", "motion"],
                 'best original score - motion picture': ["score", "motion"],
                 'best original song - motion picture': ["score", "motion"],
                 'best television series - drama': ["tv", "drama"],
                 'best performance by an actress in a television series - drama': ["actress", "tv", "drama"],
                 'best performance by an actor in a television series - drama':["actor", "tv", "drama"], 
                 'best television series - musical or comedy': ["tv", "comedy", "musical"],
                 'best performance by an actress in a television series - musical or comedy': ["actress", "tv", "comedy", "musical"],
                 'best performance by an actor in a television series - musical or comedy': ["actor", "tv", "comedy", "musical"],
                 'best mini-series or motion picture made for television': ["mini"],
                 'best performance by an actress in a mini-series or motion picture made for television': ["actress", "mini"],
                 'best performance by an actor in a mini-series or motion picture made for television': ["actor", "mini"],
                 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ["actress", "supporting", "mini"],
                 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ["actor", "supporting", "mini"]}



def containStopWord(name):
    for name_token in nltk.word_tokenize(name):
        if name_token in stopWords:
            return True
    return False


def get_names(year):
    f = open('files/gg%s.json' % year)
    data = json.load(f)
    namesDict = {}
    for i in range(0, len(data)):
        text = data[i]["text"]
        rule1 = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+ present", text)
        rule2 = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+ and [A-Z][a-z]+ [A-Z][a-z]+ present ", text)
        rules = [rule1, rule2]

        for rule in rules:
            if rule:
                for sent in rule:
                    possible_names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", sent)
                    for name in possible_names:
                        nameLower = name.lower()
                        if not containStopWord(nameLower):
                            namesDict[nameLower] = 0
    return namesDict



def get_dict_larger_than(d, threshold):
    return dict((k, v) for k, v in d.items() if v >= threshold)

def isContainAll(text, keyWords):
    present_words = ["present", "presents", "presenting", "presenter", "presenters","presented"]
    _continue = False
    newtext = ""
    for present_word in present_words:
        if present_word in text: 
            index = text.find(present_word)
            newtext = text[:]
            _continue = True
            break

    if not _continue: return False

    for keyWord in keyWords:
        if keyWord.lower() not in text:
            return False
    return True


def cleanString(s):
    return "".join(" " if i in punctuation else i for i in s.strip(punctuation))

def remove_punc(s):
    return " ".join(cleanString(i) for i in s.split())


def isContainName(text, name):
    for name_token in nltk.word_tokenize(name):
        if len(name_token) >= 3 and name_token in text: return True
    return False


def get_presenters_results(awards, year):
    # TODO: choose scripts
    scripts = []
    if year == "2013" or year == "2015":
        awards = OFFICIAL_AWARDS_1315
        scripts = AWARD_SCRIPTS_1315
    elif year == "2018" or year == "2019":
        awards = OFFICIAL_AWARDS_1819
        scripts = AWARD_SCRIPTS_1819
    else:
        print("Bad Year, expect 2013, 2015, 2018 or 2019")
        return 

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
        # print("Award: ", award)
        # print("     my   answers: ,", my_answer)
        # # print("     true answers: ", *answer_dict[award], sep = ", ")
        # print("\n")
        names = dict.fromkeys(names, 0)
    with open('gg%sresults.json' % year, 'w', encoding='utf8') as outfile:
        json.dump(result, outfile)