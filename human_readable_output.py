import json
import sys

def main():
    AWARDS = []
    if len(sys.argv)<2:
        print('Please give a year')
        return
    elif len(sys.argv)>3:
    	print("please give only one year")


    year = sys.argv[1]



    with open('gg%sresults.json'%year, 'r') as f:
        fres1 = json.load(f)

    with open('gg%sadditional_goals.json'%year, 'r') as f:
        fres2 = json.load(f)

    with open('gg%sformated_results.json'%year, 'r') as f:
        fres3 = json.load(f)


    if year == "2013" or year == "2015":
    	AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    elif year == "2018" or year == "2019":
        AWARDS = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']



    print("Hosts: ", fres1["host"])
    print("\n")
    print("Mined Awards:")
    for award in fres3["Mined_Awards"]:
    	print(award)
    print("\n")

    for AWARD in AWARDS:
        print("Award: ", AWARD) 
        print("Presenters", fres1["presenters"][AWARD])
        print("Nominees", fres1["nominees"][AWARD])
        print("Winner", fres1["winner"][AWARD])
        print("\n")


    print("Additional Goal 1: ")
    print("Best Dressed: ", fres2["best_dress"])
    print("Worst Dressed: ", fres2["worst_dress"])
    print("\n")

    print("Additional Goal 2: ")
    for key in fres2["common_sentiments"]:
    	print("Common sentimens related to host: ", key, "are: ", fres2["common_sentiments"][key])

if __name__ == '__main__':
    main()
