#!/usr/bin/python

from __future__ import print_function

# open and read a file:
def read_dict(f, cat=1, lc=False):
    """Given a file that contains one word per line
    and the name of a category,
    returns a dict (= hash) that contains each word with this category.

    Example call: msh_dic = read_dict("msh-diso-1.dic", "diso1")
    Example output: { "viral": "diso1", "virus": "diso1", ... }
    Example call: nci_dic = read_dict("msh-diso-1.dic", "diso2")
    Example output: { "acanthosis": "diso2", ... }
"""
    with open(f, "r") as inf:
        # remove \n at the end of each word
        if lc:
            return { w[:-1].casefold():cat for w in inf.readlines() }
        else:
            return { w[:-1]:cat for w in inf.readlines() }

def dict_features(dics, words):
    """Given a dictionary (or a list of dictionaries) and a list of words,
    returns the dictionary information found for each word.

    Example call: dict_features(msh_dic, ["the", "virus", "of", "acanthosis"])
    Example output: {"diso1"}

    Example call: dict_features([msh_dic, nci_dic], ["the", "virus", "of", "acanthosis"])
    Example output: {"diso1", "diso2"}"""
    features = set()            # empty set
    if not isinstance(dics, list):
        dics = [ dics ]
    for w in words:
        for d in dics:
            if w in d:
                features.add(d[w])
    return features


if __name__ == '__main__':
    msh_dict = read_dict("msh-diso-1.dic", "diso1")
    print("Dictionary length: {}: {}".format("msh_dict", len(msh_dict)))
    w = "virus"
    print("Is '{}' in the dictionary?: {}".format(w, w in msh_dict))
    w = "acanthosis"
    print("Is '{}' in the dictionary?: {}".format(w, w in msh_dict))
    f = dict_features(msh_dict, ["the", "virus", "of", "acanthosis"])
    print("Features: {}".format(f))

    nci_dict = read_dict("nci-diso-1.dic", "diso2")
    print("Dictionary length: {}: {}".format("nci_dict", len(nci_dict)))
    w = "virus"
    print("Is '{}' in the dictionary?: {}".format(w, w in nci_dict))
    w = "acanthosis"
    print("Is '{}' in the dictionary?: {}".format(w, w in nci_dict))
    f = dict_features(nci_dict, ["the", "virus", "of", "acanthosis"])
    print("Features: {}".format(f))
    

