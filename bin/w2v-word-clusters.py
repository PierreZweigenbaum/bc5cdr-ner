#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create word clusters based upon word2vec vector distance.

Pierre Zweigenbaum, LISN, CNRS, Université Paris-Saclay <pz@limsi.fr>
"""

# Program version
version = '0.1'

import os
import sys
import argparse
import logging
from gensim.models import KeyedVectors
from sklearn import cluster

# from gensim.test.utils import get_tmpfile

def w2v_to_kv(input_file, output_file):
    # load existing word2vec model, in binary word2vec format
    wv = KeyedVectors.load_word2vec_format(input_file, binary=True)
    wv.save(output_file)
    return

# load existing word2vec "KeyedVectors" saved with wv.save("path"): much faster
def load_kv(input_file):
    return KeyedVectors.load(input_file, mmap='r')

# create N clusters based on vector distance
def clusterize(wv, num_clusters, max_voc=None):
    if max_voc is None:
        X = wv[wv.vocab]
    else:
        X = wv[wv.vocab[:max_voc]]
    kmeans = cluster.KMeans(n_clusters=num_clusters)
    kmeans.fit(X)
    return kmeans

# build dictionary for word -> cluster label
def build_cluster_dict(wv, kmeans):
    w2c = {}
    for w, l in zip(wv.vocab, kmeans.labels_):
        w2c[w] = l
    return w2c

# write cluster dictionary as a tsv file
def save_cluster_dict(wv, kmeans, output_file):
    with open(output_file, "w", encoding='utf-8', newline='') as out:
        for w, l in zip(wv.vocab, kmeans.labels_):
            out.write("{}\t{}".format(w, l))
            out.write("\n")
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

    nlp = spacy.load(args.model, disable=["parser", "ner"])
    tokenize_from_list(nlp)     # parse from pretokenized list of tokens

    with open(args.output, "w", encoding='utf-8', newline='') as out:
        for s in parse_file(args.input, nlp):
            for t in s:
                out.write("\t".join(t))
                out.write("\n")
            out.write("\n")

if __name__ == '__main__':
    main()
