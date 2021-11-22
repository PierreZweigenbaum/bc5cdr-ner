# Biomedical Named Entity Recognition experiments with the BioCreative V Chemical-Disease Relation (CDR) dataset

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

Output:

        processed 124750 tokens with 9809 phrases; found: 6850 phrases; correct: 6103.
        accuracy:  95.03%; precision:  89.09%; recall:  62.22%; FB1:  73.27
                 Chemical: precision:  94.18%; recall:  63.10%; FB1:  75.57  3608
                  Disease: precision:  83.44%; recall:  61.14%; FB1:  70.57  3242

| entity type | P | R | F1 | Positive |
|---|---|---|---|---|
| Chemical | 94.18 | 63.10 | 75.57 | 3608 |
| Disease  | 83.44 | 61.14 | 70.57 | 3242 |
| total    | 89.09 | 62.22 | 73.27 |      |

- the train, devel and test TSV files contain at least a TOKEN attribute column and a LABEL gold standard column (for training and evaluation)
  - you can add more columns with extra attributes for each token (see the bin/ directory)
  - note that column numbering starts with 0
  - look at bin/tag-tsv-file-with-pos.py to discover how LEMMA and POS information was added to new columns in the corpus files with SpaCy
- the CRF engine itself creates the actual features by processing the contents of these attributes through a set of patterns defined in a template file (see the .tpl files)
  - you can test more template files:
   - ../tok-pos.tpl      *uses language-specific part-of-speech attribute in column 3*
      - requires the corpus files in BC5CDR-IOB-pos/ or in BC5CDR-IOB-pos-w2v/

Output (*language-specific POS*):

	    processed 124750 tokens with 9809 phrases; found: 7061 phrases; correct: 6291.
	    accuracy:  95.27%; precision:  89.10%; recall:  64.13%; FB1:  74.58
	    Chemical: precision:  94.19%; recall:  65.00%; FB1:  76.91  3716
	    Disease: precision:  83.44%; recall:  63.09%; FB1:  71.85  3345

| entity type | P | R | F1 | Positive |
|---|---|---|---|---|
| Chemical |  94.19 |  65.00 |  76.91  | 3716 |
| Disease |  83.44 |  63.09 |  71.85  | 3345 |
| total| 89.10 |  64.13 |  74.58 | |

Output (*universal POS*):

    processed 124750 tokens with 9809 phrases; found: 6988 phrases; correct: 6222.
    accuracy:  95.15%; precision:  89.04%; recall:  63.43%; FB1:  74.08
	     Chemical: precision:  94.28%; recall:  63.96%; FB1:  76.21  3653
	      Disease: precision:  83.30%; recall:  62.79%; FB1:  71.61  3335

| entity type | P | R | F1 | Positive |
|---|---|---|---|---|
| Chemical |  94.28 |  63.96 |  76.21  | 3653 |
| Disease |  83.30 |  62.79 |  71.61  | 3335 |
| total| 89.04 |  63.43 |  74.08 | |

   - ../tok-pos-w2v.tpl  *uses language-specific part-of-speech attribute in column 3 and word2vec cluster ID in column 4*
      - requires the corpus files in BC5CDR-IOB-pos-w2v/

Output (*language-specific POS + word2vec*):

    processed 124750 tokens with 9809 phrases; found: 7421 phrases; correct: 6613.
    accuracy:  95.59%; precision:  89.11%; recall:  67.42%; FB1:  76.76
	     Chemical: precision:  93.24%; recall:  70.92%; FB1:  80.56  4096
	      Disease: precision:  84.03%; recall:  63.16%; FB1:  72.11  3325

| entity type | P | R | F1 | Positive |
|---|---|---|---|---|
| Chemical |  93.24 |  70.92 |  80.56  | 4096 |
| Disease |  84.03 |  63.16 |  72.11  | 3325 |
| total| 89.11 |  67.42 |  76.76 | |

  - visit https://wapiti.limsi.fr/manual.html#patterns to know more about creating your own patterns
