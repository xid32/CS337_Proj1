import nltk
import json
from string import punctuation

f = open('files/gg2015.json')
data = json.load(f)

true_result = {"hosts": ["amy poehler", "tina fey"], "award_data": {"best screenplay - motion picture": {"nominees": ["zero dark thirty", "lincoln", "silver linings playbook", "argo"], "presenters": ["robert pattinson", "amanda seyfried"], "winner": "django unchained"}, "best director - motion picture": {"nominees": ["kathryn bigelow", "ang lee", "steven spielberg", "quentin tarantino"], "presenters": ["halle berry"], "winner": "ben affleck"}, "best performance by an actress in a television series - comedy or musical": {"nominees": ["zooey deschanel", "tina fey", "julia louis-dreyfus", "amy poehler"], "presenters": ["aziz ansari", "jason bateman"], "winner": "lena dunham"}, "best foreign language film": {"nominees": ["the intouchables", "kon tiki", "a royal affair", "rust and bone"], "presenters": ["arnold schwarzenegger", "sylvester stallone"], "winner": "amour"}, "best performance by an actor in a supporting role in a motion picture": {"nominees": ["alan arkin", "leonardo dicaprio", "philip seymour hoffman", "tommy lee jones"], "presenters": ["bradley cooper", "kate hudson"], "winner": "christoph waltz"}, "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["hayden panettiere", "archie panjabi", "sarah paulson", "sofia vergara"], "presenters": ["dennis quaid", "kerry washington"], "winner": "maggie smith"}, "best motion picture - comedy or musical": {"nominees": ["the best exotic marigold hotel", "moonrise kingdom", "salmon fishing in the yemen", "silver linings playbook"], "presenters": ["dustin hoffman"], "winner": "les miserables"}, "best performance by an actress in a motion picture - comedy or musical": {"nominees": ["emily blunt", "judi dench", "maggie smith", "meryl streep"], "presenters": ["will ferrell", "kristen wiig"], "winner": "jennifer lawrence"}, "best mini-series or motion picture made for television": {"nominees": ["the girl", "hatfields & mccoys", "the hour", "political animals"], "presenters": ["don cheadle", "eva longoria"], "winner": "game change"}, "best original score - motion picture": {"nominees": ["argo", "anna karenina", "cloud atlas", "lincoln"], "presenters": ["jennifer lopez", "jason statham"], "winner": "life of pi"}, "best performance by an actress in a television series - drama": {"nominees": ["connie britton", "glenn close", "michelle dockery", "julianna margulies"], "presenters": ["nathan fillion", "lea michele"], "winner": "claire danes"}, "best performance by an actress in a motion picture - drama": {"nominees": ["marion cotillard", "sally field", "helen mirren", "naomi watts", "rachel weisz"], "presenters": ["george clooney"], "winner": "jessica chastain"}, "cecil b. demille award": {"nominees": [], "presenters": ["robert downey, jr."], "winner": "jodie foster"}, "best performance by an actor in a motion picture - comedy or musical": {"nominees": ["jack black", "bradley cooper", "ewan mcgregor", "bill murray"], "presenters": ["jennifer garner"], "winner": "hugh jackman"}, "best motion picture - drama": {"nominees": ["django unchained", "life of pi", "lincoln", "zero dark thirty"], "presenters": ["julia roberts"], "winner": "argo"}, "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["max greenfield", "danny huston", "mandy patinkin", "eric stonestreet"], "presenters": ["kristen bell", "john krasinski"], "winner": "ed harris"}, "best performance by an actress in a supporting role in a motion picture": {"nominees": ["amy adams", "sally field", "helen hunt", "nicole kidman"], "presenters": ["megan fox", "jonah hill"], "winner": "anne hathaway"}, "best television series - drama": {"nominees": ["boardwalk empire", "breaking bad", "downton abbey (masterpiece)", "the newsroom"], "presenters": ["salma hayek", "paul rudd"], "winner": "homeland"}, "best performance by an actor in a mini-series or motion picture made for television": {"nominees": ["benedict cumberbatch", "woody harrelson", "toby jones", "clive owen"], "presenters": ["jessica alba", "kiefer sutherland"], "winner": "kevin costner"}, "best performance by an actress in a mini-series or motion picture made for television": {"nominees": ["nicole kidman", "jessica lange", "sienna miller", "sigourney weaver"], "presenters": ["don cheadle", "eva longoria"], "winner": "julianne moore"}, "best animated feature film": {"nominees": ["frankenweenie", "hotel transylvania", "rise of the guardians", "wreck-it ralph"], "presenters": ["sacha baron cohen"], "winner": "brave"}, "best original song - motion picture": {"nominees": ["act of valor", "stand up guys", "the hunger games", "les miserables"], "presenters": ["jennifer lopez", "jason statham"], "winner": "skyfall"}, "best performance by an actor in a motion picture - drama": {"nominees": ["richard gere", "john hawkes", "joaquin phoenix", "denzel washington"], "presenters": ["george clooney"], "winner": "daniel day-lewis"}, "best television series - comedy or musical": {"nominees": ["the big bang theory", "episodes", "modern family", "smash"], "presenters": ["jimmy fallon", "jay leno"], "winner": "girls"}, "best performance by an actor in a television series - drama": {"nominees": ["steve buscemi", "bryan cranston", "jeff daniels", "jon hamm"], "presenters": ["salma hayek", "paul rudd"], "winner": "damian lewis"}, "best performance by an actor in a television series - comedy or musical": {"nominees": ["alec baldwin", "louis c.k.", "matt leblanc", "jim parsons"], "presenters": ["lucy liu", "debra messing"], "winner": "don cheadle"}}}
true_result = {"hosts": ["amy poehler", "tina fey"], "award_data": {"best screenplay - motion picture": {"nominees": ["the grand budapest hotel", "gone girl", "boyhood", "the imitation game"], "presenters": ["bill hader", "kristen wiig"], "winner": "birdman"}, "best director - motion picture": {"nominees": ["wes anderson", "ava duvernay", "david fincher", "alejandro inarritu gonzalez"], "presenters": ["harrison ford"], "winner": "richard linklater"}, "best performance by an actress in a television series - comedy or musical": {"nominees": ["lena dunham", "edie falco", "julia louis-dreyfus", "taylor schilling"], "presenters": ["bryan cranston", "kerry washington"], "winner": "gina rodriguez"}, "best foreign language film": {"nominees": ["force majeure", "gett: the trial of viviane amsalem", "ida", "tangerines"], "presenters": ["colin farrell", "lupita nyong'o"], "winner": "leviathan"}, "best performance by an actor in a supporting role in a motion picture": {"nominees": ["robert duvall", "edward norton", "mark ruffalo"], "presenters": ["jennifer aniston", "benedict cumberbatch"], "winner": "j.k. simmons"}, "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["uzo aduba", "kathy bates", "allison janney", "michelle monaghan"], "presenters": ["jamie dornan", "dakota johnson"], "winner": "joanne froggatt"}, "best motion picture - comedy or musical": {"nominees": ["birdman", "into the woods", "pride", "st. vincent"], "presenters": ["robert downey, jr."], "winner": "the grand budapest hotel"}, "best performance by an actress in a motion picture - comedy or musical": {"nominees": ["emily blunt", "helen mirren", "julianne moore", "quvenzhane wallis"], "presenters": ["ricky gervais"], "winner": "amy adams"}, "best mini-series or motion picture made for television": {"nominees": ["the missing", "the normal heart", "olive kitteridge", "true detective"], "presenters": ["jennifer lopez", "jeremy renner"], "winner": "fargo"}, "best original score - motion picture": {"nominees": ["the imitation game", "birdman", "gone girl", "interstellar"], "presenters": ["sienna miller", "vince vaughn"], "winner": "the theory of everything"}, "best performance by an actress in a television series - drama": {"nominees": ["claire danes", "viola davis", "julianna margulies", "robin wright"], "presenters": ["anna faris", "chris pratt"], "winner": "ruth wilson"}, "best performance by an actress in a motion picture - drama": {"nominees": ["jennifer aniston", "felicity jones", "rosamund pike", "reese witherspoon"], "presenters": ["matthew mcconaughey"], "winner": "julianne moore"}, "cecil b. demille award": {"nominees": [], "presenters": ["don cheadle", "julianna margulies"], "winner": "george clooney"}, "best performance by an actor in a motion picture - comedy or musical": {"nominees": ["ralph fiennes", "bill murray", "joaquin phoenix", "christoph waltz"], "presenters": ["amy adams"], "winner": "michael keaton"}, "best motion picture - drama": {"nominees": ["foxcatcher", "the imitation game", "selma", "the theory of everything"], "presenters": ["meryl streep"], "winner": "boyhood"}, "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["alan cumming", "colin hanks", "bill murray", "jon voight"], "presenters": ["katie holmes", "seth meyers"], "winner": "matt bomer"}, "best performance by an actress in a supporting role in a motion picture": {"nominees": ["jessica chastain", "keira knightley", "emma stone", "meryl streep"], "presenters": ["jared leto"], "winner": "patricia arquette"}, "best television series - drama": {"nominees": ["downton abbey (masterpiece)", "game of thrones", "the good wife", "house of cards"], "presenters": ["adam levine", "paul rudd"], "winner": "the affair"}, "best performance by an actor in a mini-series or motion picture made for television": {"nominees": ["martin freeman", "woody harrelson", "matthew mcconaughey", "mark ruffalo"], "presenters": ["jennifer lopez", "jeremy renner"], "winner": "billy bob thornton"}, "best performance by an actress in a mini-series or motion picture made for television": {"nominees": ["jessica lange", "frances mcdormand", "frances o'connor", "allison tolman"], "presenters": ["kate beckinsale", "adrien brody"], "winner": "maggie gyllenhaal"}, "best animated feature film": {"nominees": ["big hero 6", "the book of life", "the boxtrolls", "the lego movie"], "presenters": ["kevin hart", "salma hayek"], "winner": "how to train your dragon 2"}, "best original song - motion picture": {"nominees": ["big eyes", "noah", "annie", "the hunger games: mockingjay - part 1"], "presenters": ["prince"], "winner": "selma"}, "best performance by an actor in a motion picture - drama": {"nominees": ["steve carell", "benedict cumberbatch", "jake gyllenhaal", "david oyelowo"], "presenters": ["gwyneth paltrow"], "winner": "eddie redmayne"}, "best television series - comedy or musical": {"nominees": ["girls", "jane the virgin", "orange is the new black", "silicon valley"], "presenters": ["bryan cranston", "kerry washington"], "winner": "transparent"}, "best performance by an actor in a television series - drama": {"nominees": ["clive owen", "liev schreiber", "james spader", "dominic west"], "presenters": ["david duchovny", "katherine heigl"], "winner": "kevin spacey"}, "best performance by an actor in a television series - comedy or musical": {"nominees": ["louis c.k.", "don cheadle", "ricky gervais", "william h. macy"], "presenters": ["jane fonda", "lily tomlin"], "winner": "jeffrey tambor"}}}
# Hardcoded Awards
OFFICIAL_AWARDS = ['cecil b. demille award', 
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





AWARD_SCRIPTS = {'cecil b. demille award': ["cecil", "demille"],
                 'best motion picture - drama': ['motion', 'drama'],
                 'best performance by an actress in a motion picture - drama': ["motion", "drama"],
                 'best performance by an actor in a motion picture - drama': ["motion", "drama"],
                 'best motion picture - comedy or musical': ["motion", "comedy", "musical"],
                 'best performance by an actress in a motion picture - comedy or musical': ["comedy", "musical"],
                 'best performance by an actor in a motion picture - comedy or musical': ["comedy", "musical"],
                 'best animated feature film': ["animated"],
                 'best foreign language film': ["foreign language"],
                 'best performance by an actress in a supporting role in a motion picture': ["supporting", "motion"],
                 'best performance by an actor in a supporting role in a motion picture': ["supporting", "motion"],
                 'best director - motion picture': ["director", "motion"],
                 'best screenplay - motion picture': ["screenplay", "motion"],
                 'best original score - motion picture': ["score", "motion"],
                 'best original song - motion picture': ["song", "motion"],
                 'best television series - drama': ["tv", "drama"],
                 'best performance by an actress in a television series - drama': ["tv", "drama"],
                 'best performance by an actor in a television series - drama':["tv", "drama"], 
                 'best television series - comedy or musical': ["tv", "comedy", "musical"],
                 'best performance by an actress in a television series - comedy or musical': ["tv", "comedy", "musical"],
                 'best performance by an actor in a television series - comedy or musical': ["tv", "comedy", "musical"],
                 'best mini-series or motion picture made for television': ["mini"],
                 'best performance by an actress in a mini-series or motion picture made for television': ["mini"],
                 'best performance by an actor in a mini-series or motion picture made for television': ["mini"],
                 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ["supporting", "mini"],
                 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ["supporting", "mini"]}


def cleanString(s):
    return "".join(" " if i in punctuation else i for i in s.strip(punctuation))

def remove_punc(s):
    return " ".join(cleanString(i) for i in s.split())

def get_dict_larger_than(d, threshold):
    return dict((k, v) for k, v in d.items() if v >= threshold)


def isContainAll(text, keyWords):
    present_words = ["present", "presents", "presenting", "presenter", "presenters","presented"]
    _continue = False
    for present_word in present_words:
        if present_word in text: 
            _continue = True
            break

    if not _continue: return False

    for keyWord in keyWords:
        if keyWord.lower() not in text:
            return False
    return True

def get_answers():
    answer_dict= {}
    answer = true_result
    for key in answer["award_data"]:
        answer_dict[key] = answer["award_data"][key]["presenters"]
    return answer_dict


# TODO: Mine the names instead of hard code 
def get_names():
    num_presenters = 0
    names = {}
    answer = true_result
    for key in answer["award_data"]:
        for presenter in answer["award_data"][key]["presenters"]:
            names[presenter] = 0
            num_presenters += 1
    return names

names = get_names()


print("len: ", len(data))
def v2(awards, scripts, names, answer_dict):
    result = true_result
    k = 0
    for award in OFFICIAL_AWARDS:
        print(award)
        for i in range(0, len(data)):
            text = remove_punc(data[i]["text"].lower())
            keyWords = scripts[award]
            if isContainAll(text, keyWords):
                for key in names:
                    if remove_punc(key).lower() in text:
                        names[key] += 1
        new_dict = get_dict_larger_than(names, 1)
        result['award_data'][award]["presenters"] = sorted(new_dict, key=new_dict.get, reverse=True)[:2]
        print("Award: ", award)
        print("     my   answers: ,", sorted(new_dict, key=new_dict.get, reverse=True)[:2])
        print("     true answers: ", *answer_dict[award], sep = ", ")
        print("\n")
        names = dict.fromkeys(names, 0)
        k += 1
    return result

result = v2(OFFICIAL_AWARDS, AWARD_SCRIPTS, names, get_answers())
with open('gg2015answers.json', 'w', encoding='utf8') as outfile:
    json.dump(result, outfile)
