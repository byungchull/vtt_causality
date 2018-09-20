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

path = "/Users/u.hyeyeon/Dropbox/_VTT/dataset/FilmCorpus2.0/imsdb_raw_nov_2015/"
sid = SentimentIntensityAnalyzer()

for genreFolder in next(os.walk(path))[1]:
    print genreFolder
    if (genreFolder in ("")):
        continue

    verbList = []
    verbSentList = []
    vpList = []
    vpSentList = []
    for files in next(os.walk(path+genreFolder))[2]:
        print "\t"+files
        f = open(path + genreFolder + "/" + files, "r")
        plotText = f.read()
        f.close()

        plotText = re.sub('<!--.*?>.*?-->', '', plotText, 0, re.I | re.S)
        plotText = re.sub('<.+?>', '', plotText, 0, re.I | re.S)

        sentList = [x.replace("\n"," ") for x in nltk.sent_tokenize(plotText.replace("\t",""))]

        for strSentence in sentList:
            #print(strSentence)
            for word, pos in tag(strSentence) :
                if pos in ("VB","VBD","VBG","VBN","VBP","VBZ") :
                    word = str(lemma(word))

                    if (word not in ("be", "do", "let", "begin", "have", "try", "start")):
                        verbList.append(word)
                        verbSentList.append(sid.polarity_scores(word))


                        #con.execute("INSERT OR IGNORE INTO verbList VALUES(?, ?)", (lemma(word),0,))
                        #con.execute("UPDATE verbList SET count = count + 1 WHERE verb=?", (lemma(word),))

            a = parse(strSentence, relations=True, lemmata=True)
            #pprint(a)

            sentence = Sentence(a)
            for i in range(0,len(sentence.verbs)-1) :
                strVP = str(' '.join(sentence.verbs[i].lemmata))
                if (strVP not in ("be", "do", "let", "begin", "have", "try", "start")):
                    vpList.append(strVP)
                    vpSentList.append(sid.polarity_scores(strVP))

            #print(sentence.relations)
            #print(sentence.subjects)
            #print(sentence.objects)
            #print(sentence.verbs)
            #print(sentence.chunk)

            # sqlite3 insert : subject / objects / verbs / CPC / Sentiment
            #   genre, wordCount, filename, sentence
            #   subject : Chunk('he/NP-SBJ-1'), Chunk('you/NP-SBJ-2')]
            #   objects : [Chunk('it/NP-OBJ-2')]
            #   verbs : [Chunk('would n't talk/VP-1'), Chunk('saw/VP-2')]
            #   CPC :
            #   Sentiment : {'neg': 0.0, 'neu': 0.853, 'pos': 0.147, 'compound': 0.1406}

            #ret.write(strSentence+"\n")

    con = sqlite3.connect("causalRelation.db")
    con.isolation_level = None  # auto commit
    cursor = con.cursor()

    #   init table
    #cursor.execute("DROP TABLE IF EXISTS verbList")
    #cursor.execute("CREATE TABLE verbList (verb TEXT NOT NULL PRIMARY KEY, count INTEGER DEFAULT(1), senti_neg TEXT, senti_neu TEXT, senti_pos TEXT, senti_com TEXT)")

    #cursor.execute("DROP TABLE IF EXISTS vpList")
    #cursor.execute("CREATE TABLE vpList (vp TEXT NOT NULL PRIMARY KEY, count INTEGER DEFAULT(1), senti_neg TEXT, senti_neu TEXT, senti_pos TEXT, senti_com TEXT)")

    verbDic = {}
    for i in range(0,len(verbList)):

        if (verbList[i] in verbDic):
            verbDic[verbList[i]] = verbDic[verbList[i]] + 1
            con.execute("UPDATE verbList SET count = count + 1 WHERE verb=? AND genre=?", (verbList[i],genreFolder,))
        else :
            verbDic[verbList[i]] = 1
            con.execute("INSERT INTO verbList(verb, count, senti_neg, senti_neu, senti_pos, senti_com, genre) VALUES(?, ?, ?, ?, ?, ?, ?)", (verbList[i], 1, str(verbSentList[i]["neg"]),str(verbSentList[i]["neu"]),str(verbSentList[i]["pos"]),str(verbSentList[i]["compound"]), genreFolder, ))

    vpDic = {}
    for i in range(0,len(vpList)):

        if (vpList[i] in vpDic):
            vpDic[vpList[i]] = vpDic[vpList[i]] + 1
            con.execute("UPDATE vpList SET count = count + 1 WHERE vp=? AND genre=?", (vpList[i], genreFolder,))
        else :
            vpDic[vpList[i]] = 1
            con.execute("INSERT INTO vpList(vp, count, senti_neg, senti_neu, senti_pos, senti_com, genre) VALUES(?, ?, ?, ?, ?, ?, ?)", (vpList[i], 1, str(verbSentList[i]["neg"]),str(verbSentList[i]["neu"]),str(verbSentList[i]["pos"]),str(verbSentList[i]["compound"]),genreFolder,))
    con.close()

