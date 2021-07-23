# Biomedical Named Entity Recognition experiments with BioCreative V Chemical-Disease Relation (CDR)
## Installation instructions
### Supervised sequence classifier: the Wapiti CRF (linux)
  - download Wapiti 1.5.0 from https://wapiti.limsi.fr/#download
    - wget https://wapiti.limsi.fr/wapiti-1.5.0.tar.gz
  - $ tar xzf wapiti-1.5.0.tar.gz
  - $ cd wapiti-1.5.0
  - installation instructions are in INSTALL:
    - compilation (requires a C compiler)
      - $ make
    - installation:
      - system-wide installation (into /usr/bin/ --- requires root privilege):
	      - $ sudo make install
      - user-local installation (into ~/bin/)
	      - $ make install PREFIX=/home/myself
### Supervised sequence classifier: Optional: the NeuroNLP2 neural CNN-BiLSTM-CRF
  - install a virtual environment manager for Python
    - install miniconda
      - download from https://docs.conda.io/en/latest/miniconda.html
      - install according to https://docs.continuum.io/anaconda/install/
  - create a virtual environment to install the suitable Python modules
    - $ conda create --name nnlp2 python=3.6
    - $ conda activate nnlp2
  - install the required modules
    - $ conda install pytorch=1.3.1 gensim python-Levenshtein
