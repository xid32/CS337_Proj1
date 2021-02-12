'''Version 0.35'''

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from imdb import IMDb
import Levenshtein as lev
import json
import regex
from collections import Counter
import itertools
import string
import nltk
import demoji
from nltk.chunk import conlltags2tree, tree2conlltags
import spacy
from pathlib import Path
import textdistance
from difflib import SequenceMatcher
import time
import copy
from textblob import TextBlob
import numpy as np
import random
import get_nominees

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

OFFICIAL_AWARDS = []
TWEETS = []
CLEAN_DATA = []
TWEET_BY_AWARD_DICT = dict()
ia = IMDb()
GG_RESULT = {}


def get_tweets(year):
    global TWEETS
    try:
        f = open('gg' + str(year) + '.json')
        data = json.load(f)
        TWEETS = [tweet['text'] for tweet in data]
        # if year == "2013" or year == "2015"or year == "2018"or year == "2019":
        #    f = open('gg'+year+'.json')
        #    data = json.load(f)
        #    TWEETS = [tweet['text'] for tweet in data]
        #    #return TWEETS
        # else:
        #    with open('gg'+year+'.json', encoding='utf8') as json_file:
        #        data = [json.loads(line) for line in json_file]
        #    TWEETS = [tweet['text'] for tweet in data]
        # return TWEETS
        TWEETS.sort()
    #         TWEETS = list(TWEETS for TWEETS,_ in itertools.groupby(TWEETS))
    except:
        return False


def load_data(year):
    global OFFICIAL_AWARDS
    global TWEETS
    if not OFFICIAL_AWARDS or not TWEETS:
        print("get")
        get_tweets(year)
        if year == "2013" or year == "2015":  # or year == "2020":
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
        else:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    else:
        print("pass load")


def strip_all_entities(text):
    new_str = string.punctuation
    new_str = new_str.replace('-', '')
    new_str = new_str.replace(',', '')
    new_str += '“'
    entity_prefixes = ['@', '#']
    for separator in new_str:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def data_clean():
    global TWEETS
    global CLEAN_DATA
    if not CLEAN_DATA:
        for tweet_text in TWEETS:
            # tweet_text = tweet['text']
            no_http = re.sub('http://\S+|https://\S+', '', tweet_text)
            remove_tag = strip_all_entities(no_http)
            new_item = re.sub(r'–', '-', remove_tag)
            new_item = re.sub(r'[Tt].[Vv].', 'television', new_item)
            new_item = re.sub(r'[Tt][Vv]', 'television', new_item)
            new_item = re.sub(r'RT ', '', new_item)
            # new_item = new_item.translate(str.maketrans('', '', string.punctuation))
            CLEAN_DATA.append(new_item.lower())
        # CLEAN_DATA.sort()
        # CLEAN_DATA = list(set(CLEAN_DATA))
    else:
        print("pass clean")




def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return []#hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    load_data(year)
    awards = OFFICIAL_AWARDS
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    get_nominees.get_nominees(year)

    f = open(str(year) + '_nominees' + '.json')
    nominees = json.load(f)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = {}
    load_data(year)
    for award in OFFICIAL_AWARDS:
        winners[award] = []
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = {}
    load_data(year)
    for award in OFFICIAL_AWARDS:
        presenters[award] = []
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    main()
