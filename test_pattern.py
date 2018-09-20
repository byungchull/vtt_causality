#   supported python 2.7
#
#   https://www.clips.uantwerpen.be/pages/pattern-en#parser
#       With relations=True each word is annotated with a role tag (e.g., -SBJ for subject or -OBJ for).
#       With lemmata=True each word is annotated with its base form.
#       With tokenize=False, punctuation marks will not be separated from words.
#
#   https://www.clips.uantwerpen.be/pages/MBSP-tags
#       Relation tags
#       . sentence subject(SBJ)
#       . sentence object(OBJ)
#
#   python -m pip install vaderSentiment
#

import os
import re
import nltk
from nltk.corpus.reader import WORD
from pattern.en import parse, tree, pprint, Sentence, parsetree, Text, Chunk, tag
from pattern.search import search
from pattern.text import Sentence
from nltk.sentiment.vader import SentimentIntensityAnalyzer

"""
s = 'The mobile web is more important than mobile apps.'
s = parsetree(s)
for sentence in s:
    for chunk in sentence.chunks:
        for word in chunk.words:
            print (word),
    print()

"""

#s = parsetree('The mobile web is more important than mobile apps.', relations=True, lemmata=True)
#print repr(s)
#print parse('I ate pizza.').split()

#s = 'The mobile web is more important than mobile apps.'
#pprint(parse(s, relations=True, lemmata=True))


path = "/Users/u.hyeyeon/Dropbox/_VTT/dataset/FilmCorpus2.0/imsdb_raw_nov_2015/Action"
sid=SentimentIntensityAnalyzer()

#for files in next(os.walk(path))[2]:
files = "15minutes.txt"
f = open(path + "/" + files, "r")
plotText = f.read()
f.close()

plotText = re.sub('<!--.*?>.*?-->', '', plotText, 0, re.I | re.S)
plotText = re.sub('<.+?>', '', plotText, 0, re.I | re.S)

sentList = [x.replace("\n"," ") for x in nltk.sent_tokenize(plotText.replace("\t",""))]

for strSentence in sentList:

    for word, pos in tag(strSentence) :
        if pos in ("VB","VBD","VBG","VBN","VBP","VBZ"): # Retrieve all adjectives.
            print ("=====================>>>>> ",word,pos)
        else :
            print (word, pos)

    print(strSentence)
    a = parse(strSentence, relations=True, lemmata=True)
    pprint(a)

    sentence = Sentence(a)
    print(sentence.verbs)
    print
    print

    #print(sentence.relations)
    #print(sentence.subjects)
    #print(sentence.objects)
    #print(sentence.verbs)
    #print(sentence.chunk)

    sentScore = sid.polarity_scores(strSentence)

    # sqlite3 insert : subject / objects / verbs / CPC / Sentiment
    #   genre, wordCount, filename, sentence
    #   subject : Chunk('he/NP-SBJ-1'), Chunk('you/NP-SBJ-2')]
    #   objects : [Chunk('it/NP-OBJ-2')]
    #   verbs : [Chunk('would n't talk/VP-1'), Chunk('saw/VP-2')]
    #   CPC :
    #   Sentiment : {'neg': 0.0, 'neu': 0.853, 'pos': 0.147, 'compound': 0.1406}

    #ret.write(strSentence+"\n")

