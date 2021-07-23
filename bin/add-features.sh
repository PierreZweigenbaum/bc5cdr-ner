#!/bin/bash

mkdir -p BC5CDR-IOB-w2v BC5CDR-IOB-pos BC5CDR-IOB-pos-w2v
DICT=embeddings/pmc-20150131.tok.sent.200.5.1000.1e-3.cld

for f in train # devel test
do
    echo $f
    time python bin/tag-tsv-file-with-dict.py -d $DICT BC5CDR-IOB/$f.tsv BC5CDR-IOB-w2v/$f.tsv
    time python bin/tag-tsv-file-with-pos.py BC5CDR-IOB-w2v/$f.tsv BC5CDR-IOB-pos-w2v/$f.tsv
    # time python bin/tag-tsv-file-with-pos.py BC5CDR-IOB/$f.tsv BC5CDR-IOB-pos/$f.tsv
done
