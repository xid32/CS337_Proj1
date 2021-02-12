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
import emoji
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
            # print('cleaning')
            # print(tweet_text)
            # remove_emoji = emoji.get_emoji_regexp().sub(r'', tweet_text.encode('utf8').decode('utf8'))
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


def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    get_tweets(year)
    global GG_RESULT
    if "nominees" in GG_RESULT:
        return GG_RESULT["nominees"]

    load_data(year)
    data_clean()
    stop_words = set(stopwords.words('english'))
    # reward dict
    award_dict = {}
    nominee = {}
    for award_name in OFFICIAL_AWARDS:
        award_dict[award_name] = {}
        reduced_award_name = award_name.replace("award", "")
        reduced_award_name = reduced_award_name.replace("made for television", "television")
        reduced_award_name = reduced_award_name.replace(" - ", " ")
        reduced_award_name = reduced_award_name.replace(",", "")
        reduced_award_name = reduced_award_name.replace(" b. ", " ")
        reduced_award_name = reduced_award_name.replace("performance", "")
        reduced_award_name = reduced_award_name.replace(" by ", " ")
        reduced_award_name = reduced_award_name.replace(" an ", " ")
        reduced_award_name = reduced_award_name.replace(" in a ", " ")
        reduced_award_name = reduced_award_name.replace(" or ", " ")
        reduced_award_name = reduced_award_name.replace(" film", "")
        reduced_award_name = reduced_award_name.replace(" role ", " ")
        reduced_award_name = reduced_award_name.replace(" series ", " ")
        reduced_award_name = reduced_award_name.replace(" for ", " ")
        reduced_award_name = reduced_award_name.replace("best ", "")
        reduced_award_name = reduced_award_name.replace("mini-series", "series")
        reduced_award_name = reduced_award_name.replace("feature", "")
        reduced_award_name = reduced_award_name.replace("motion picture", "")
        if "act" in award_name and "television" in award_name:
            reduced_award_name = reduced_award_name.replace("television", "")
        award_dict[award_name]['search'] = reduced_award_name.split()
        award_dict[award_name]['prohibit'] = []
        if "motion picture" in award_name and "television" not in award_name:
            award_dict[award_name]['prohibit'].append("television")
        if "act" not in award_name:
            award_dict[award_name]['prohibit'].append("actor")
            award_dict[award_name]['prohibit'].append("actress")
        if "drama" not in award_name:
            award_dict[award_name]['prohibit'].append("drama")
        if "comedy" not in award_name:
            award_dict[award_name]['prohibit'].append("comedy")
        if "musical" not in award_name:
            award_dict[award_name]['prohibit'].append("musical")
        if "act" in award_name and "television" in award_name:
            award_dict[award_name]['prohibit'].append("motion")
            award_dict[award_name]['prohibit'].append("picture")
        nominee[award_name] = []

        # reward pattern
    # forward
    search_not_win = re.compile(r"(.*)(?:(?:not win))")
    search_win = re.compile(r"(.*)(?:(?:win))")
    search_deserves_to_win = re.compile(r"(.*)(?:(?:deserves to win))")
    search_deserved_to_win = re.compile(r"(.*)(?:(?:deserved to win))")
    search_deserves_a = re.compile(r"(.*)(?:(?:deserves a))")
    search_is_nominated = re.compile(r"(.*)(?:(?:is nominated))")
    search_was_nominated = re.compile(r"(.*)(?:(?:was nominated))")
    search_missed_out = re.compile(r"(.*)(?:(?:missed out))")
    search_misses_out = re.compile(r"(.*)(?:(?:misses out))")
    search_nominated_for = re.compile(r"(?:(?:nominated for))(.*)")
    search_should_have_won = re.compile(r"(.*)(?:(?:should have won))")
    search_winner_in_my = re.compile(r"(.*)(?:(?:winner in my))")
    search_won_t_win = re.compile(r"(.*)(?:(?:won t win))")
    search_doesn_t_win = re.compile(r"(.*)(?:(?:doesn t win))")
    search_should_win = re.compile(r"(.*)(?:(?:sho?u?ld win))")
    search_better_win = re.compile(r"(.*)(?:(?:better win))")
    search_not_get = re.compile(r"(.*)(?:(?:not get))")
    search_was_robbed = re.compile(r"(.*)(?:(?:was robbed))")
    search_beats_forw = re.compile(r"(.*)(?:(?:beats))")

    # backward
    search_nominee = re.compile(r"(?:(?:nominee ))(.*)")
    search_preferred = re.compile(r"(?:(?:preferred ))(.*)")
    search_prediction = re.compile(r"(?:(?:prediction))(.*)")
    search_beats = re.compile(r"(?:(?:beats ))(.*)")
    search_should_have_gone_to = re.compile(r"(?:(?:should have gone to ))(.*)")
    stop_word = ['did', 'the', 'who', 'regrettably', 'when', 'me', 'if', 'omg', 'wtf', 'wonderful', 'but', 'though',
                 'believe', 'i think', 'best', 'is', 'won', 'for', 'that', 'this', 'prediction', 'why', 'supporting',
                 'actor', 'actress', 'to win', 'original song', 'night', 'evening', 'drama', 'film', 'director', 'it s',
                 'or', 'had', 'award', 'he', 'amp', 'televisions']
    stop_splitter = re.compile(
        r'\bdid\b|\bthe\b|\bwho\b|\bwhen\b|\bregrettably\b|\bme\b|\bif\b|\bomg\b|\bwtf\b|\bwonderful\b|\bbut\b|\bthough\b|\bbelieve\b|\bi think\b|\bbest\b|\bis\b|\bwon\b|\bfor\b|\bthat\b|\bthis\b|\bprediction\b|\bwhy\b|\bsupporting\b|\bactor\b|\bactress\b|\bsho?u?ld\b|\bto win\b|\boriginal song\b|\bnight\b|\bevening\b|\bdrama\b|\bfilms?\b|\bdirector\b|\bit s\b|\bor\b|\bhad\b|\baward\b|\bs?he\b|\bamp\b|\bcomedy\b|\bmusical\b|\bout\b|\bwins?\b|\bs\b|\btelevisions?\b|\banimated\b|\bmovies?\b|\bpicture\b|\bnominees?\b|\bforeign language\b|\bmotion\b|\awards?\b|\bwhere\b|\bin a\b|\bwinner\b|\bcan t\b|\baffair\b|\bshow\b|\btonight\b|\b-\b|\bi saw\b|\bdo you think\b')

    def search_pattern(relist, inputstr, idx):
        if len(re.findall(relist, inputstr)) > 0:
            for substr in re.findall(relist, inputstr):
                tmp = re.split(stop_splitter, substr)
                tmp_clean = [x.strip() for x in tmp if x != "" and x != " "]
                # newstr = list(filter("", re.split(stop_splitter, substr)))[-1].strip()
                # print(substr)
                if len(tmp_clean) > 0:
                    newstr = tmp_clean[idx]
                    if len(newstr.split()) <= 3 and newstr not in stop_words and newstr not in string.punctuation:
                        # print(newstr)
                        if "golden" in newstr or "globes" in newstr:
                            continue
                        nominee[award].append(newstr)

    nominee = {}
    for award_name in OFFICIAL_AWARDS:
        nominee[award_name] = []
    for award in award_dict:
        # print(award)
        # print(award_dict[award]['search'])
        # print("----------------------")
        if award == 'cecil b. demille award':
            continue
        name_list = []
        for tweet in CLEAN_DATA:
            # search perfect match
            if all(word in tweet.lower() for word in award_dict[award]['search']) and not any(
                    word in tweet.lower() for word in
                    award_dict[award]['prohibit']) and 'oscar' not in tweet.lower() and 'disney' not in tweet.lower():
                search_pattern(search_not_win, tweet.lower(), -1)
                # search_pattern(search_win, tweet.lower(), -1)
                search_pattern(search_deserves_to_win, tweet.lower(), -1)
                search_pattern(search_deserved_to_win, tweet.lower(), -1)
                search_pattern(search_deserves_a, tweet.lower(), -1)
                search_pattern(search_is_nominated, tweet.lower(), -1)
                search_pattern(search_was_nominated, tweet.lower(), -1)
                search_pattern(search_missed_out, tweet.lower(), -1)
                search_pattern(search_misses_out, tweet.lower(), -1)
                search_pattern(search_should_have_won, tweet.lower(), -1)
                search_pattern(search_winner_in_my, tweet.lower(), -1)
                search_pattern(search_won_t_win, tweet.lower(), -1)
                search_pattern(search_better_win, tweet.lower(), -1)
                search_pattern(search_not_get, tweet.lower(), -1)
                search_pattern(search_was_robbed, tweet.lower(), -1)
                # search_pattern(search_beats_forw, tweet.lower(), -1)

                search_pattern(search_nominee, tweet.lower(), 0)
                search_pattern(search_preferred, tweet.lower(), 0)
                search_pattern(search_prediction, tweet.lower(), 0)
                search_pattern(search_beats, tweet.lower(), 0)
                search_pattern(search_should_have_gone_to, tweet.lower(), 0)

    nominees = copy.deepcopy(nominee)
    for award in nominees:
        nominees[award] = list(set(nominees[award]))
    GG_RESULT["nominees"] = nominees
    with open(year + '_nominees.json', 'w') as f:
        json.dump(nominees, f)