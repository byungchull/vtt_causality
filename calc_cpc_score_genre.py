#   supported python 2.7
#

import os
import re
import sqlite3
import math
from decimal import Decimal
from fractions import Fraction

con = sqlite3.connect("causalRelation.db")
con.isolation_level = None  # auto commit
cursor = con.cursor()

cursor.execute("pragma synchronous=off")

cursor.execute("SELECT eventPair,substr(eventPair,0, instr(eventPair,'_')) AS evt1,"+
               "substr(eventPair,instr(eventPair,'_')+1,length(eventPair)) AS evt2,"+
               "(SELECT COUNT FROM verbList WHERE verb=substr(eventPair,0, instr(eventPair,'_')) AND genre=a.genre) AS evt1_cnt,"+
               "(SELECT COUNT FROM verbList WHERE verb=substr(eventPair,instr(eventPair,'_')+1,length(eventPair)) AND genre=a.genre) AS evt2_cnt,"+
               "(SELECT SUM(COUNT) FROM verbList WHERE genre='Short') AS tot_cnt, count, genre "+
               "FROM pmiScoreGenre AS a WHERE genre='Short'")
# exec : Action, Drama, Thriller, Mystery, Fantasy, Sci-Fi, Family, Comedy, Crime, Adventure
#       Animation, Romance, Horror, War, Musical, Western, Music, Film-Noir, Biography, History, Sport, Short
rows = cursor.fetchall()

i = 0;
for row in rows:
    i+=1
    print i
    eventPair = str(row[0]).split("_")
    if (len(eventPair) == 2 and eventPair[0] != "" and eventPair[1] != "" and row[3] != None and row[4] != None) :
        pmiScore = round(math.log(((Decimal.from_float(row[3])/Decimal.from_float(row[5])) + (Decimal.from_float(row[4])/Decimal.from_float(row[5]))) / ((Decimal.from_float(row[3]) / Decimal.from_float(row[5])) * (Decimal.from_float(row[4]) / Decimal.from_float(row[5])))),2)

        #print row

        cursor.execute("SELECT count, eventPair, (SELECT SUM(count) FROM pmiScoreGenre WHERE genre='"+row[7]+"') AS pmi_tot FROM pmiScoreGenre WHERE genre='"+row[7]+"' AND eventPair=\""+row[2].replace("\"","")+"_"+row[1].replace("\"","")+"\"")
        pairRows = cursor.fetchall()

        cpScore = pmiScore                                                      # pmiScore == cpScore ? event2->event1 is none


        for pairCnt in pairRows:
            #print ("2 :", pairCnt)
            if (pairCnt[0] > 0):
                cpScore = round(math.log((Decimal.from_float(row[6]) / Decimal.from_float(pairCnt[2]))/ (Decimal.from_float(pairCnt[0])/Decimal.from_float(pairCnt[2]))),2) + pmiScore

                con.execute("UPDATE pmiScoreGenre SET pmi=?, cp=? WHERE eventPair=? AND genre=?", (pmiScore, cpScore, row[0], row[7],))
                print (pmiScore, cpScore, row[0], row[7])
        #print (row[0], pmiScore, cpScore)

con.close()