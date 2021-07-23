#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Add features to a TSV file.
Use SpaCy for lemma and part-of-speech.

Pierre Zweigenbaum, LISN, CNRS, Université Paris-Saclay <pz@limsi.fr>
"""

import os
import sys
import argparse
import logging
import spacy

# Program version
version = '0.1'

def read_tsv_dict(file):
    d = {}
    with open(file, "r", encoding='utf-8', newline='') as tsv:
        for l in tsv:
            l = l[:-1]
            kv = l.split('\t')
            if len(kv) != 2:
                logging.warning("Dictionary entry should have exactly two tab-separated fields instead of {}".format(len(kv)))
            else:
                k, v = kv
                d[k] = v
    return d

def tsv_reader(file):
    with open(file, "r", encoding='utf-8', newline='') as tsv:
        # sents = []
        sent = []
        for l in tsv:
            l = l[:-1]
            if l == '':
                # sents.append(sent)
                yield sent
                sent = []
            else:
                sent.append(l.split('\t'))
    return # sents

def enrich_sentence_with_dict(s, d, oov='_'):
    """:INPUT s is a sentence: a sequence of tokens, in which each token is a sequence with the token and its pre-set attributes
    :INPUT d is a dictionary: token->feature_value
    :INPUT oov is the feature value if a token is out of the vocabulary of the dictionary

    Adds to each token the feature value found in the dictionary, '_' otherwise"""
    new_s = []
    for t in s:
        tok = t[0]
        new_t = [tok]
        f = (d[tok] if tok in d else oov)
        new_t.append(f)
        new_t.extend(t[1:])
        new_s.append(new_t)
    return new_s

def add_feature(f, d):
    i = 0
    for s in tsv_reader(f):
        toks = [r[0] for r in s]
        yield enrich_sentence_with_dict(s, d)
        i += 1
    return

def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)

    groupI = parser.add_argument_group('Input')
    groupI.add_argument("input", help="name of input TSV file")
    groupI.add_argument("output", help="name of output TSV file")

    groupP = parser.add_argument_group('Processing')
    groupP.add_argument("-d", "--dict", required=True,
                        help="Dictionary file in TSV format: word<tab>value")

    groupS = parser.add_argument_group('Special')
    groupS.add_argument("-q", "--quiet", action="store_true",
                        help="suppress reporting progress info")
    groupS.add_argument("--debug", action="store_true",
                        help="print debug info")
    groupS.add_argument("-v", "--version", action="version",
                        version='%(prog)s ' + version,
                        help="print program version")

    args = parser.parse_args()

    FORMAT = '%(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT)

    logger = logging.getLogger()
    if not args.quiet:
        logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logging.info("Reading dictionary '{}'".format(args.dict))
    wdict = read_tsv_dict(args.dict)

    logging.info("Adding dictionary values as features to {}".format(args.input))
    with open(args.output, "w", encoding='utf-8', newline='') as out:
        for s in add_feature(args.input, wdict):
            for t in s:
                out.write("\t".join(t))
                out.write("\n")
            out.write("\n")

if __name__ == '__main__':
    main()
