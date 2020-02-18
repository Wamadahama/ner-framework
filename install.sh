#!/usr/bin/sh
mkdir packages
cd packages

pip install pandas
pip install numpy
pip install scikitlearn
pip install nltk 
pip install tensorflow
pip install keras
pip install seqeval
pip install flask

git clone https://www.github.com/keras-team/keras-contrib.git
cd keras-contrib
python setup.py install

cd .. 
