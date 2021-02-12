#Use https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
#as refernece about building the NaiveBayesClassifier

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import json
from nltk.corpus import stopwords

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def clean(tweet):
    t = re.split('RT\s\@\S+\:\s',tweet,1)
    if len(t)>1:
        return clean(t[len(t)-1])
    else:
        return t[0]

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def get_dress(year):
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, 1)
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, -1)
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    if year == 2013:
        f = open('/Users/apple/Downloads/gg2013.json')
    else:
        f = open('/Users/apple/Downloads/gg2015.json')
    data = json.load(f)
    new_data = []
    result = {}
    for i in data:
        custom_tweet = clean(i['text'])
        custom_tweet = custom_tweet.split('#')[0]
        custom_tweet = custom_tweet.split('http')[0]
        if re.match('.+.+wearing.+.+', custom_tweet):
            name = custom_tweet.split('wearing')[0]
            name = name.split()
            isall = True
            for j in name:
                if not j[0].isupper():
                    isall = False
                    break
            name = [w for w in name if not w.lower() in stop_words and w.lower() !="i'm"]
            name = [w[0] for w in pos_tag(name) if w[1] == 'NNP']
            
            if isall and len(name)>1:
                name = ' '.join(name)
                custom_tokens = remove_noise(word_tokenize(custom_tweet.split('wearing')[1]))
                stop_words = set(stopwords.words('english'))
                custom_tokens = [w for w in custom_tokens if not w in stop_words]
                if name in result.keys():
                    result[name]+= classifier.classify(dict([token, True] for token in custom_tokens))
                else:
                    result[name] = classifier.classify(dict([token, True] for token in custom_tokens))
    a = list(result.values())
    b = list(result.keys())

    maxt = 0
    mint = 0
    h = ''
    l = ''
    for x,y in zip(a,b):
        if x>maxt:
            maxt = x
            h = y
        if x<mint:
            mint = x
            l = y
    print({'Best Dressed:':h,'Worst Dressed:':l})



if __name__ == "__main__":
    get_dress(2013)
    get_dress(2015)
