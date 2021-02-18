import json
import sys
from get_dress import get_dress as gd
from get_sentiments import get_sentiments_results

def get_answers(year):
    with open('gg%sresults.json'%year, 'r') as f:
        fres = json.load(f)
    return fres

def get_hosts(year):
    return get_answers(year)['host']


def main():
    if len(sys.argv)<2:
        print('Please give a year')
        return
    elif len(sys.argv)>3:
    	print("please give only one year")


    year = sys.argv[1]

    # Additional Goal 1: Get Dress
    print("Getting Best Dress...")
    h,l = gd.get_dress(year)
    print('	Best Dressed: ',h)
    print('	Worst Dressed: ' ,l)

    # Additional Goal 2: Get Common sentiments for hosts
    print("Getting sentiments related to hosts...")
    hosts = get_hosts(year)
    sent = get_sentiments_results.get_sentiments(hosts,year)
    for h in hosts:
        print('	Common sentiments to host',h ,':' ,sent[h]['words'])

    additional_goal = {}
    additional_goal["best_dress"] = h
    additional_goal["worst_dress"] = l
    additional_goal["common_sentiments"] = {}
    for host in hosts:
        additional_goal["common_sentiments"][host] = sent[h]['words']

    with open('gg%sadditional_goals.json' % year, 'w', encoding='utf8') as outfile:
        json.dump(additional_goal, outfile, indent=4)



if __name__ == '__main__':
    main()