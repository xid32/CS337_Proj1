import nltk
import json
from string import punctuation
import regex as re
import time

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def clean(tweet):
    t = re.split('RT\s\@\S+\:\s',tweet,1)
    if len(t)>1:
        return clean(t[len(t)-1])
    else:
        return t[0]

def cleanString(s):
    
    return "".join(" " if i in punctuation else i for i in s.strip(punctuation))

def remove_punc(s):
    return " ".join(cleanString(i) for i in s.split())


def find_s(x,y):
    
    X_list = x.split()
    Y_list = y.split() 

    l1 =[];l2 =[] 

    X_set = {w for w in X_list} 
    Y_set = {w for w in Y_list} 

    rvector = X_set.union(Y_set) 
    for w in rvector: 
        if w in X_set: l1.append(1)
        else: l1.append(0) 
        if w in Y_set: l2.append(1)
        else: l2.append(0) 

    c = 0
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 

    return cosine

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''

    t = time.time()
    if year == '2013':
        f = open('/Users/apple/Downloads/gg2013.json')
    else:
        f = open('/Users/apple/Downloads/gg2015.json')

    data = json.load(f)


    OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315


    new_data = []
    for i in data:
        s = clean(i['text'])
        s = cleanString(s)
        new_data.append(remove_punc(s))

    winners = []

    for i in OFFICIAL_AWARDS:
        winners.append({})

    for i in new_data:
        if re.match('.+.+wins.+.+for.+.+', i):
            
            name = i.split('wins')[0].lstrip().rstrip()
            name = re.split('[:/#@]+',name)
            name = name[len(name)-1].split('http')
            name = name[len(name)-1]
            award = i.split('for')[1].lower().lstrip().rstrip()

            name = name.split()
            name = [w for w in name if w!='Goldenglobes' and w!='GoldenGlobes' and w!='goldenglobes']
            name = ' '.join(name)
            
            if re.match('^best', award):
                maxs = 0
                pos = -1
                award = re.split('[:/#@.]+',award)
                award = award[0].split('http')
                award = award[0].split('goldenglobes')
                award = award[0]
                for j in range(len(OFFICIAL_AWARDS)):
                    temp = find_s(award.lower(),OFFICIAL_AWARDS[j])
                    if temp>maxs:
                        maxs = temp
                        pos = j
                if pos == -1:
                    continue
                if name in winners[pos].keys():
                    winners[pos][name]+=1
                else:
                    winners[pos][name] = 1

        elif re.match('.+.+\sgoes\sto.+.+',i):
            words = re.split('\sgoes\sto',i)
            if re.match('^best',words[0].lower().lstrip()):
                award = words[0].lower().lstrip().rstrip()
                name = words[1].lstrip().rstrip()
                w = re.split('[:/.#@]+',name)
                w = w[0].split('http')
                w = w[0].split('GoldenGlobes')
                names = w[0]

                temp = names.split()

                name = ''
                for i in temp:
                    if i[0].isupper():
                        name+=i
                        name+=' '
                    else:
                        break
                name = name.split()
                name = [w for w in name if w!='Goldenglobes' and w!='GoldenGlobes' and w!='goldenglobes']
                name = ' '.join(name)

                maxs = 0
                pos = -1
                for j in range(len(OFFICIAL_AWARDS)):
                    temp = find_s(award.lower(),OFFICIAL_AWARDS[j])
                    if temp>maxs:
                        maxs = temp
                        pos = j
                if pos == -1:
                    continue
                if name in winners[pos].keys():
                    winners[pos][name]+=1
                else:
                    winners[pos][name] = 1

    result = {}

    for i in range(len(winners)):

        result[OFFICIAL_AWARDS[i]] = ''
        if bool(winners[i]):

            a = list(winners[i].values())
            b = list(winners[i].keys())

            maxt = 0
            n = ''
            for x,y in zip(a,b):
                if x>maxt:
                    maxt = x
                    n = y
            result[OFFICIAL_AWARDS[i]] = n
    print(time.time()-t)

    return result

def main():
    result = get_winner(2013)
    with open('gg%sresults.json' % 2013, 'w', encoding='utf8') as outfile:
        json.dump(result, outfile)
    result = get_winner(2015)
    with open('gg%sresults.json' % 2015, 'w', encoding='utf8') as outfile:
        json.dump(result, outfile)
    return

if __name__ == "__main__":
    main()
