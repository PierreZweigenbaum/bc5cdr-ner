#!/bin/bash

# Usage:
# ./train-test-eval.sh PATTERN-FILE CORPUS-DIR
# ./train-test-eval.sh ../tok-pos.tpl ../../BC5CDR-IOB-pos
# assumes conlleval.pl is in ../

WAPITI=/vol/datailes/tools/ml/wapiti/cur/wapiti # update for your installation

PATTERNS=${1:-"../tok.tpl"}
BC5CDR=${2:-"../../BC5CDR-IOB"}
# BC5CDR=../../BC5CDR-IOB
# BC5CDR=../../BC5CDR-IOB-pos
THREADS=30			# update for your machine
# PATTERNS=../tok.tpl
PAT=$(basename $PATTERNS .tpl)

# train
time $WAPITI train -t $THREADS -p $PATTERNS -a rprop -d $BC5CDR/devel.tsv $BC5CDR/train.tsv bc5cdr-iob-train-$PAT-rprop.mod

# test
time $WAPITI label -m bc5cdr-iob-train-$PAT-rprop.mod $BC5CDR/test.tsv bc5cdr-iob-test-train-$PAT-rprop.tsv

# eval
../conlleval.pl -d '\t' <bc5cdr-iob-test-train-$PAT-rprop.tsv >bc5cdr-iob-test-train-$PAT-rprop.eval
