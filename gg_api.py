'''Version 0.35'''
import json
import os
from get_awards import allAwards
from get_hosts import host
from nominees import get_nominees as gs
from get_winners import get_winners as gw
from get_presenters import get_presenters_results as gr
from get_dress import get_dress as gd
from get_sentiments import get_sentiments_results
import time

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_answers(year):
    with open('gg%sresults.json'%year, 'r') as f:
        fres = json.load(f)
    return fres

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return get_answers(year)['host']

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return get_answers(year)['awards']

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    gs.get_nominees(year)
    f = open(str(year) + '_nominees' + '.json')
    nominees = json.load(f)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return get_answers(year)['winner']

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return get_answers(year)['presenters']

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    years = ['2013','2015']
    for year in years:
        ####Host#########
        filename = '../gg'+year+'.json'
        tweets = json.load(open(filename))
        hosts = host.get_hosts(tweets)
        ##################
        ####Award#########
        awards = []
        if year == '2013' or year == '2015':
            award_names = OFFICIAL_AWARDS_1315
        else:
            award_names = OFFICIAL_AWARDS_1819
        filename = '../gg'+year+'.json'
        tweets = json.load(open(filename))
        awards = allAwards.get_allAwards(tweets,year)
        ##################
        ####Presenter#########
        if year == '2013' or year == '2015':
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
        else:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
        gr.get_presenters_results(OFFICIAL_AWARDS, year)
        with open('gg%sresults.json'%year, 'r') as f:
            fres = json.load(f)
        result = {}
        for award in OFFICIAL_AWARDS:
            result[award] = fres[award]["Presenters"]
        ##################
        ####Winner#########
        winners = gw.get_winner(year)
        ##################
        output = []
        h,l = gd.get_dress(year)
        print('Host: ',hosts)
        for j in OFFICIAL_AWARDS_1315:
            print()
            print('Award:',j)
            print('Presenters:',result[j])
            print('Winner:',winners[j])
        print()
        print('Best Dressed: ',h)
        print('Worst Dressed: ' ,l)
        print()
        sent = get_sentiments_results.get_sentiments(hosts,year)
        for h in hosts:
            print('Common sentiments to host',h ,':' ,sent[h]['words'])
        
        with open('gg%sresults.json' % year, 'w', encoding='utf8') as outfile:
            json.dump({'host':hosts,'awards':awards,'presenters':result,'winner':winners,'Best Dressed:':h,
                        'Worst Dressed:':l,'sentiment':sent}, outfile)
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    pre_ceremony()
    return

if __name__ == '__main__':
    main()