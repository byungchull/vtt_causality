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
#-*- coding: utf-8 -*-
import os
import re
import nltk
from nltk.corpus.reader import WORD
from pattern.en import parse, tree, pprint, Sentence, parsetree, Text, Chunk, tag, conjugate, lemma, lexeme
from pattern.search import search
from pattern.text import Sentence
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3

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

#path = "/Users/u.hyeyeon/Dropbox/_VTT/dataset/bbc/"
#path = "/Users/u.hyeyeon/Dropbox/_VTT/dataset/FilmCorpus2.0/imsdb_raw_nov_2015/"

path = "E:/Dropbox/_VTT/dataset/bbc/"

sid=SentimentIntensityAnalyzer()

con = sqlite3.connect("Corpus.db")
con.isolation_level = None  # auto commit
cursor = con.cursor()

fileSeq=0
genreFolder="entertainment"
files = "289.txt"


fileSeq = fileSeq + 1
#con.execute("INSERT INTO fileTBL (seq, genre, fileName, corpus) VALUES(?, ?, ?, ?)", (fileSeq, genreFolder, files, 'BBC', ))

f = open(path + genreFolder + "/" + files, "r")
plotText = f.read()
f.close()

plotText = re.sub('<!--.*?>.*?-->', '', plotText, 0, re.I | re.S)
plotText = re.sub('<.+?>', '', plotText, 0, re.I | re.S)
sentList = [x.replace("\n"," ") for x in nltk.sent_tokenize(plotText.decode('utf-8').replace("\t",""))]

sentenceSeq = 0
for strSentence in sentList:
    #print("strSentence : ", strSentence)

    sentenceSeq+=1
    sentiment = sid.polarity_scores(strSentence)
    #con.execute("INSERT INTO sentenceTBL (fileSeq, seq, sentence, obj, pos, neg, neu, com) VALUES(?, ?, ?, ?, ?, ?, ?)", (fileSeq, sentenceSeq, strSentence, sentiment["neg"], sentiment["neu"], sentiment["compound"]))

    a = parse(strSentence, relations=True, lemmata=True)
    #pprint(a)

    sentence = Sentence(a)

    listVP = []
    listOBJ = []
    listSBJ = []
    # solved Dictionary's Key None
    if (None in sentence.relations["VP"] or None in sentence.relations["SBJ"] or None in sentence.relations["OBJ"]):
        listVP.append("")
        listOBJ.append("")
        listSBJ.append("")

    for key, val in sentence.relations["VP"].items():
        if ("None" in str(key)):
            listVP[0] = val
        else :
            listVP.append(val)

    for key, val in sentence.relations["SBJ"].items():
        if ("None" in str(key)):
            listSBJ[0] = val
        listSBJ.append(val)

    for key, val in sentence.relations["OBJ"].items():
        if ("None" in str(key)):
            listOBJ[0] = val
        listOBJ.append(val)

    maxID = max(len(listVP), len(listOBJ), len(listSBJ))
    if (maxID > 0) :
        for i in range(maxID):
            try:
                subject = ' '.join(listSBJ[i].lemmata)
            except :
                subject = ""

            try:
                verbs = ' '.join(listVP[i].lemmata)
            except :
                verbs = ""

            try:
                objects = ' '.join(listOBJ[i].lemmata)
            except :
                objects = ""



            print(subject, verbs, objects, i)

            #con.execute("INSERT INTO ChunkTBL (fileSeq, sentSeq, id, sbj, vp, obj) VALUES(?, ?, ?, ?, ?, ?)", (fileSeq, sentenceSeq, i, subject, verbs, objects),  )
        print ("====================================================")

    #print strVP
    #print(sentence.relations)
    #print(sentence.subjects)
    #print(sentence.objects)
    #print(sentence.verbs)
    #print(sentence.chunk)

con.close()

'''
con = sqlite3.connect("causalRelation.db")
con.isolation_level = None  # auto commit
cursor = con.cursor()

prevVerb = verbList[0]
verbDic = {}
for i in range(1,len(verbList)-1):
    if (verbList[i] not in ("be","do","let","begin","have","try","start")):
        print (prevVerb, "_", verbList[i])

        if (prevVerb+"_"+verbList[i] in verbDic):
            verbDic[prevVerb+"_"+verbList[i]] = verbDic[prevVerb+"_"+verbList[i]] + 1
            con.execute("UPDATE pmiScoreGenre SET count = count + 1 WHERE genre=? AND eventPair=?", (genreFolder, prevVerb + "_" + verbList[i],))
        else :
            verbDic[prevVerb+"_"+verbList[i]] = 1
            con.execute("INSERT INTO pmiScoreGenre(eventPair, count, genre) VALUES(?, ?, ?)", (prevVerb + "_" + verbList[i], 1, genreFolder, ))
        prevVerb = verbList[i]


print ("verbList =====================>>>>> ", verbList)
print ("vpList =====================>>>>> ", vpList)
print ("verbDic =====================>>>>> ", verbDic)

    # sqlite3 insert : subject / objects / verbs / CPC / Sentiment
    #   genre, wordCount, filename, sentence
    #   subject : Chunk('he/NP-SBJ-1'), Chunk('you/NP-SBJ-2')]
    #   objects : [Chunk('it/NP-OBJ-2')]
    #   verbs : [Chunk('would n't talk/VP-1'), Chunk('saw/VP-2')]
    #   CPC :
    #   Sentiment : {'neg': 0.0, 'neu': 0.853, 'pos': 0.147, 'compound': 0.1406}

    #ret.write(strSentence+"\n")
'''