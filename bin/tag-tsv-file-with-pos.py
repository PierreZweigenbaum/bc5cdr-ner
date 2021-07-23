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

# inspired from https://github.com/explosion/spaCy/issues/42
# make SpaCy read directly from a list of tokens
def tokenize_from_list(nlp):
    old_tokenizer = nlp.tokenizer 
    nlp.tokenizer = lambda l: old_tokenizer.tokens_from_list(l)

# not used here
def read_tsv_file(file):
    with open(file, "r", encoding='utf-8', newline='') as tsv:
        sents = []
        sent = []
        for l in tsv:
            l = l[:-1]
            if l == '':
                sents.append(sent)
                sent = []
            else:
                sent.append(l.split('\t'))
    return sents

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

def enrich_sentence(s, doc):
    """:INPUT s is a sentence: a sequence of tokens, in which each token is a sequence with the token and its pre-set attributes
    :INPUT doc is a SpaCy Doc produced by analyzing the sequence of tokens
    
    Adds to each token the information computed by SpaCy on: LEMMA, Universal POS, Language-specific POS"""
    new_s = []
    i = 0
    for t in doc:
        new_t = [s[i][0]]
        new_t.extend([t.lemma_, t.pos_, t.tag_])
        new_t.extend(s[i][1:])
        new_s.append(new_t)
        i += 1
    return new_s

def parse_file(f, nlp):
    i = 0
    for s in tsv_reader(f):
        toks = [r[0] for r in s]
        doc = nlp(toks)
        if len(doc) != len(toks):
            logging.warning("Number of SpaCy tokens does not match the input number of tokens in sentence {}: input {} vs SpaCy {}".format(i, toks, doc))
        yield enrich_sentence(s, doc)
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
    groupP.add_argument("-m", "--model", default="en_core_web_sm",
                        help="SpaCy model to use. Default: %(default)s)")

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

    logging.info("Reading SpaCy model '{}'".format(args.model))
    nlp = spacy.load(args.model, disable=["parser", "ner"])
    tokenize_from_list(nlp)     # parse from pretokenized list of tokens

    logging.info("Adding SpaCy LEMMA, POS values as features to {}".format(args.input))
    with open(args.output, "w", encoding='utf-8', newline='') as out:
        for s in parse_file(args.input, nlp):
            for t in s:
                out.write("\t".join(t))
                out.write("\n")
            out.write("\n")

if __name__ == '__main__':
    main()
