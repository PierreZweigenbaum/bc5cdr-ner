# Biomedical Named Entity Recognition experiments with BioCreative V Chemical-Disease Relation (CDR)

## Installation instructions

### Supervised sequence classifier: the Wapiti CRF (linux)

- download Wapiti 1.5.0 from https://wapiti.limsi.fr/#download

        $ wget https://wapiti.limsi.fr/wapiti-1.5.0.tar.gz
        $ tar xzf wapiti-1.5.0.tar.gz
        $ cd wapiti-1.5.0

- installation instructions are in INSTALL:
    - compilation (requires a C compiler)

        $ make

    - system-wide installation (into /usr/bin/ --- requires root privilege):

        $ sudo make install

    - or user-local installation (into ~/bin/)

        $ make install PREFIX=/home/myself

### Supervised sequence classifier: Optional: the NeuroNLP2 neural CNN-BiLSTM-CRF

  - install a virtual environment manager for Python
    - install miniconda
     - download from https://docs.conda.io/en/latest/miniconda.html
     - install according to https://docs.continuum.io/anaconda/install/
  - create a virtual environment to install the suitable Python modules

        $ conda create --name nnlp2 python=3.6
        $ conda activate nnlp2

  - install the required modules

        $ conda install pytorch=1.3.1 gensim python-Levenshtein

## Experiments

### Supervised sequence classification with the Wapiti CRF

    cd wapiti/experiments

- update train-test-eval.sh with:
  - the path for the wapiti executable
  - the maximum number of threads you wish to allocate to training
- run a NER experiment with only token-based features

        $ ./train-test-eval.sh ../tok.tpl ../../BC5CDR-IOB

- this will train a CRF model with these features on the training corpus ../../BC5CDR-IOB/train.tsv, then test it on the test corpus ../../BC5CDR-IOB/test.tsv, and evaluate its entity recognition and classification performance with ../conlleval.pl
  - the result files are created in the current directory

        $ cat bc5cdr-iob-test-train-tok-rprop.eval

        processed 124750 tokens with 9809 phrases; found: 6850 phrases; correct: 6103.
        accuracy:  95.03%; precision:  89.09%; recall:  62.22%; FB1:  73.27
                 Chemical: precision:  94.18%; recall:  63.10%; FB1:  75.57  3608
                  Disease: precision:  83.44%; recall:  61.14%; FB1:  70.57  3242

- the train, devel and test TSV files contain at least a TOKEN attribute column and a LABEL gold standard column (for training and evaluation)
  - you can add more columns with extra attributes for each token (see the bin/ directory)
  - note that column numbering starts with 0
  - look at bin/tag-tsv-file-with-pos.py to discover how LEMMA and POS information was added to new columns in the corpus files with SpaCy
- the CRF engine itself creates the actual features by processing the contents of these attributes through a set of patterns defined in a template file (see the .tpl files)
  - you can test more template files:
   - ../tok-pos.tpl      *uses language-specific part-of-speech attribute in column 3*
      - requires the corpus files in BC5CDR-IOB-pos/ or in BC5CDR-IOB-pos-w2v/
   - ../tok-pos-w2v.tpl  *uses language-specific part-of-speech attribute in column 3 and word2vec cluster ID in column 4*
      - requires the corpus files in BC5CDR-IOB-pos-w2v/
  - visit https://wapiti.limsi.fr/manual.html#patterns to know more about creating your own patterns
