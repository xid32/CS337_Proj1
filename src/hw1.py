import nltk
import json
# f = open('files/gg2013.json')
# data = json.load(f)
import re


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

def containStopWord(name):
    for name_token in nltk.word_tokenize(name):
        if name_token in stopWords:
            return True
    return False


def get_names_v3(year):
    f = open('files/gg%s.json' % year)
    data = json.load(f)
    namesDict = {}
    for i in range(0, len(data)):
        text = data[i]["text"]
        rule1 = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+ present", text)
        rule2 = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+ and [A-Z][a-z]+ [A-Z][a-z]+ present ", text)
        if rule1:
            for sent in rule1:
                possible_names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", sent)
                for name in possible_names:
                    nameLower = name.lower()
                    if not containStopWord(nameLower):
                        namesDict[nameLower] = 0

        if rule2: 
            for sent in rule2:
                possible_names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", sent)
                for name in possible_names:
                    nameLower = name.lower()
                    if not containStopWord(nameLower):
                        namesDict[nameLower] = 0
    return namesDict

def get_2013_names():
    names = {}
    true_result_2013 = {"hosts": ["amy poehler", "tina fey"], "award_data": {"best screenplay - motion picture": {"nominees": ["zero dark thirty", "lincoln", "silver linings playbook", "argo"], "presenters": ["robert pattinson", "amanda seyfried"], "winner": "django unchained"}, "best director - motion picture": {"nominees": ["kathryn bigelow", "ang lee", "steven spielberg", "quentin tarantino"], "presenters": ["halle berry"], "winner": "ben affleck"}, "best performance by an actress in a television series - comedy or musical": {"nominees": ["zooey deschanel", "tina fey", "julia louis-dreyfus", "amy poehler"], "presenters": ["aziz ansari", "jason bateman"], "winner": "lena dunham"}, "best foreign language film": {"nominees": ["the intouchables", "kon tiki", "a royal affair", "rust and bone"], "presenters": ["arnold schwarzenegger", "sylvester stallone"], "winner": "amour"}, "best performance by an actor in a supporting role in a motion picture": {"nominees": ["alan arkin", "leonardo dicaprio", "philip seymour hoffman", "tommy lee jones"], "presenters": ["bradley cooper", "kate hudson"], "winner": "christoph waltz"}, "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["hayden panettiere", "archie panjabi", "sarah paulson", "sofia vergara"], "presenters": ["dennis quaid", "kerry washington"], "winner": "maggie smith"}, "best motion picture - comedy or musical": {"nominees": ["the best exotic marigold hotel", "moonrise kingdom", "salmon fishing in the yemen", "silver linings playbook"], "presenters": ["dustin hoffman"], "winner": "les miserables"}, "best performance by an actress in a motion picture - comedy or musical": {"nominees": ["emily blunt", "judi dench", "maggie smith", "meryl streep"], "presenters": ["will ferrell", "kristen wiig"], "winner": "jennifer lawrence"}, "best mini-series or motion picture made for television": {"nominees": ["the girl", "hatfields & mccoys", "the hour", "political animals"], "presenters": ["don cheadle", "eva longoria"], "winner": "game change"}, "best original score - motion picture": {"nominees": ["argo", "anna karenina", "cloud atlas", "lincoln"], "presenters": ["jennifer lopez", "jason statham"], "winner": "life of pi"}, "best performance by an actress in a television series - drama": {"nominees": ["connie britton", "glenn close", "michelle dockery", "julianna margulies"], "presenters": ["nathan fillion", "lea michele"], "winner": "claire danes"}, "best performance by an actress in a motion picture - drama": {"nominees": ["marion cotillard", "sally field", "helen mirren", "naomi watts", "rachel weisz"], "presenters": ["george clooney"], "winner": "jessica chastain"}, "cecil b. demille award": {"nominees": [], "presenters": ["robert downey, jr."], "winner": "jodie foster"}, "best performance by an actor in a motion picture - comedy or musical": {"nominees": ["jack black", "bradley cooper", "ewan mcgregor", "bill murray"], "presenters": ["jennifer garner"], "winner": "hugh jackman"}, "best motion picture - drama": {"nominees": ["django unchained", "life of pi", "lincoln", "zero dark thirty"], "presenters": ["julia roberts"], "winner": "argo"}, "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["max greenfield", "danny huston", "mandy patinkin", "eric stonestreet"], "presenters": ["kristen bell", "john krasinski"], "winner": "ed harris"}, "best performance by an actress in a supporting role in a motion picture": {"nominees": ["amy adams", "sally field", "helen hunt", "nicole kidman"], "presenters": ["megan fox", "jonah hill"], "winner": "anne hathaway"}, "best television series - drama": {"nominees": ["boardwalk empire", "breaking bad", "downton abbey (masterpiece)", "the newsroom"], "presenters": ["salma hayek", "paul rudd"], "winner": "homeland"}, "best performance by an actor in a mini-series or motion picture made for television": {"nominees": ["benedict cumberbatch", "woody harrelson", "toby jones", "clive owen"], "presenters": ["jessica alba", "kiefer sutherland"], "winner": "kevin costner"}, "best performance by an actress in a mini-series or motion picture made for television": {"nominees": ["nicole kidman", "jessica lange", "sienna miller", "sigourney weaver"], "presenters": ["don cheadle", "eva longoria"], "winner": "julianne moore"}, "best animated feature film": {"nominees": ["frankenweenie", "hotel transylvania", "rise of the guardians", "wreck-it ralph"], "presenters": ["sacha baron cohen"], "winner": "brave"}, "best original song - motion picture": {"nominees": ["act of valor", "stand up guys", "the hunger games", "les miserables"], "presenters": ["jennifer lopez", "jason statham"], "winner": "skyfall"}, "best performance by an actor in a motion picture - drama": {"nominees": ["richard gere", "john hawkes", "joaquin phoenix", "denzel washington"], "presenters": ["george clooney"], "winner": "daniel day-lewis"}, "best television series - comedy or musical": {"nominees": ["the big bang theory", "episodes", "modern family", "smash"], "presenters": ["jimmy fallon", "jay leno"], "winner": "girls"}, "best performance by an actor in a television series - drama": {"nominees": ["steve buscemi", "bryan cranston", "jeff daniels", "jon hamm"], "presenters": ["salma hayek", "paul rudd"], "winner": "damian lewis"}, "best performance by an actor in a television series - comedy or musical": {"nominees": ["alec baldwin", "louis c.k.", "matt leblanc", "jim parsons"], "presenters": ["lucy liu", "debra messing"], "winner": "don cheadle"}}}
    answer = true_result_2013
    for key in answer["award_data"]:
        for presenter in answer["award_data"][key]["presenters"]:
            names[presenter] = 0
    return names

def get_2015_names():
    names = {}
    true_result_2015 = {"hosts": ["amy poehler", "tina fey"], "award_data": {"best screenplay - motion picture": {"nominees": ["the grand budapest hotel", "gone girl", "boyhood", "the imitation game"], "presenters": ["bill hader", "kristen wiig"], "winner": "birdman"}, "best director - motion picture": {"nominees": ["wes anderson", "ava duvernay", "david fincher", "alejandro inarritu gonzalez"], "presenters": ["harrison ford"], "winner": "richard linklater"}, "best performance by an actress in a television series - comedy or musical": {"nominees": ["lena dunham", "edie falco", "julia louis-dreyfus", "taylor schilling"], "presenters": ["bryan cranston", "kerry washington"], "winner": "gina rodriguez"}, "best foreign language film": {"nominees": ["force majeure", "gett: the trial of viviane amsalem", "ida", "tangerines"], "presenters": ["colin farrell", "lupita nyong'o"], "winner": "leviathan"}, "best performance by an actor in a supporting role in a motion picture": {"nominees": ["robert duvall", "edward norton", "mark ruffalo"], "presenters": ["jennifer aniston", "benedict cumberbatch"], "winner": "j.k. simmons"}, "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["uzo aduba", "kathy bates", "allison janney", "michelle monaghan"], "presenters": ["jamie dornan", "dakota johnson"], "winner": "joanne froggatt"}, "best motion picture - comedy or musical": {"nominees": ["birdman", "into the woods", "pride", "st. vincent"], "presenters": ["robert downey, jr."], "winner": "the grand budapest hotel"}, "best performance by an actress in a motion picture - comedy or musical": {"nominees": ["emily blunt", "helen mirren", "julianne moore", "quvenzhane wallis"], "presenters": ["ricky gervais"], "winner": "amy adams"}, "best mini-series or motion picture made for television": {"nominees": ["the missing", "the normal heart", "olive kitteridge", "true detective"], "presenters": ["jennifer lopez", "jeremy renner"], "winner": "fargo"}, "best original score - motion picture": {"nominees": ["the imitation game", "birdman", "gone girl", "interstellar"], "presenters": ["sienna miller", "vince vaughn"], "winner": "the theory of everything"}, "best performance by an actress in a television series - drama": {"nominees": ["claire danes", "viola davis", "julianna margulies", "robin wright"], "presenters": ["anna faris", "chris pratt"], "winner": "ruth wilson"}, "best performance by an actress in a motion picture - drama": {"nominees": ["jennifer aniston", "felicity jones", "rosamund pike", "reese witherspoon"], "presenters": ["matthew mcconaughey"], "winner": "julianne moore"}, "cecil b. demille award": {"nominees": [], "presenters": ["don cheadle", "julianna margulies"], "winner": "george clooney"}, "best performance by an actor in a motion picture - comedy or musical": {"nominees": ["ralph fiennes", "bill murray", "joaquin phoenix", "christoph waltz"], "presenters": ["amy adams"], "winner": "michael keaton"}, "best motion picture - drama": {"nominees": ["foxcatcher", "the imitation game", "selma", "the theory of everything"], "presenters": ["meryl streep"], "winner": "boyhood"}, "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["alan cumming", "colin hanks", "bill murray", "jon voight"], "presenters": ["katie holmes", "seth meyers"], "winner": "matt bomer"}, "best performance by an actress in a supporting role in a motion picture": {"nominees": ["jessica chastain", "keira knightley", "emma stone", "meryl streep"], "presenters": ["jared leto"], "winner": "patricia arquette"}, "best television series - drama": {"nominees": ["downton abbey (masterpiece)", "game of thrones", "the good wife", "house of cards"], "presenters": ["adam levine", "paul rudd"], "winner": "the affair"}, "best performance by an actor in a mini-series or motion picture made for television": {"nominees": ["martin freeman", "woody harrelson", "matthew mcconaughey", "mark ruffalo"], "presenters": ["jennifer lopez", "jeremy renner"], "winner": "billy bob thornton"}, "best performance by an actress in a mini-series or motion picture made for television": {"nominees": ["jessica lange", "frances mcdormand", "frances o'connor", "allison tolman"], "presenters": ["kate beckinsale", "adrien brody"], "winner": "maggie gyllenhaal"}, "best animated feature film": {"nominees": ["big hero 6", "the book of life", "the boxtrolls", "the lego movie"], "presenters": ["kevin hart", "salma hayek"], "winner": "how to train your dragon 2"}, "best original song - motion picture": {"nominees": ["big eyes", "noah", "annie", "the hunger games: mockingjay - part 1"], "presenters": ["prince"], "winner": "selma"}, "best performance by an actor in a motion picture - drama": {"nominees": ["steve carell", "benedict cumberbatch", "jake gyllenhaal", "david oyelowo"], "presenters": ["gwyneth paltrow"], "winner": "eddie redmayne"}, "best television series - comedy or musical": {"nominees": ["girls", "jane the virgin", "orange is the new black", "silicon valley"], "presenters": ["bryan cranston", "kerry washington"], "winner": "transparent"}, "best performance by an actor in a television series - drama": {"nominees": ["clive owen", "liev schreiber", "james spader", "dominic west"], "presenters": ["david duchovny", "katherine heigl"], "winner": "kevin spacey"}, "best performance by an actor in a television series - comedy or musical": {"nominees": ["louis c.k.", "don cheadle", "ricky gervais", "william h. macy"], "presenters": ["jane fonda", "lily tomlin"], "winner": "jeffrey tambor"}}}
    answer = true_result_2015
    for key in answer["award_data"]:
        for presenter in answer["award_data"][key]["presenters"]:
            names[presenter] = 0
    return names

# namesDict = get_names_v3()

# presenters = get_2015_names()
# for presenter in presenters:
#     if presenter not in namesDict:
#         print(presenter)

# print(namesDict)



