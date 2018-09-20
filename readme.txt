1. insert_verb_vp.py
    FilmCorpus2.0 의 Action 폴더의 파일들에서 동사와 동사구 찾아서 데이터베이스에 입력 (동사원형 또는 동사구 원형, 사용회수, sentiment value{neg, neu, pos, com})
    데이터베이스 : sqlite3, causalRelation.db
    테이블명 : verbList(verb, count, senti_neg, senti_neu, senti_pos, senti_com), vpList(vp, count, senti_neg, senti_neu, senti_pos, senti_com)

2. insert_verb_pair.py
    FilmCorpus2.0 의 Action 폴더의 파일들에서 동사와 동사구를 찾아서 동사가 사용된 순서로 pair를 정하고, 데이터베이스에 입력 (동사원형 또는 동사구 원형 pair, 사용회수, 'Action')
    데이터베이스 : sqlite3, causalRelation.db
    테이블명 : pmiScore(eventPair, count, genre)

3. update_pmi_score.py
    event pair를 조회해서 event 별 확률을 계산하고, log 계산해서 pmi score에 update
    cp 계산해서 cp score에 update
    cpc 계산해서 cpc score에 업데이트
    동사구(vp)는 사용하지 않음

=============================================================
DROP TABLE fileTBL;
CREATE TABLE fileTBL (
	seq INTEGER PRIMARY KEY,
	genre TEXT NOT NULL,
	fileName TEXT NOT NULL,
	corpus TEXT NOT NULL
);
DROP TABLE sentenceTBL;
CREATE TABLE sentenceTBL (
	fileSeq INTEGER NOT NULL,
	seq INTEGER NOT NULL,
	sentence TEXT NOT NULL,
	pos TEXT,
	neg TEXT,
	neu TEXT,
	com TEXT,
	PRIMARY KEY (seq, fileSeq)
);
DROP TABLE chunkTBL;
CREATE TABLE chunkTBL (
	fileSeq INTEGER NOT NULL,
	sentSeq INTEGER NOT NULL,
	id INTEGER NOT NULL,
	SBJ TEXT,
	VP TEXT,
	OBJ TEXT,
	PRIMARY KEY (fileSeq, sentSeq, id)
);

strSentence="Through the window of a moving vehicle, we see a series of small, middle-class houses."
a = parse(strSentence, relations=True, lemmata=True)
sentence = Sentence(a)
pprint(a)
          WORD   TAG    CHUNK   ROLE   ID     PNP    LEMMA

       Through   IN     PP      -      -      PNP    through
           the   DT     NP      -      -      PNP    the
        window   NN     NP ^    -      -      PNP    window
            of   IN     PP      -      -      -      of
             a   DT     -       -      -      -      a
        moving   VBG    VP      -      1      -      move
       vehicle   NN     NP      OBJ    1      -      vehicle
             ,   ,      -       -      -      -      ,
            we   PRP    NP      SBJ    2      -      we
           see   VBP    VP      -      2      -      see
             a   DT     NP      OBJ    2      -      a
        series   NN     NP ^    OBJ    2      -      series
            of   IN     PP      -      -      -      of
         small   JJ     ADJP    -      -      -      small
             ,   ,      -       -      -      -      ,
  middle-class   NN     NP      -      -      -      middle-class
        houses   NNS    NP ^    -      -      -      house
             .   .      -       -      -      -      .
sentence.subjects
sentence.relations

sentence.relations
    {'SBJ': {2: Chunk('we/NP-SBJ-2')}, 'VP': {1: Chunk('moving/VP-1'), 2: Chunk('see/VP-2')}, 'OBJ': {1: Chunk('vehicle/NP-OBJ-1'), 2: Chunk('a series/NP-OBJ-2')}}
sentence.relations["VP"]
    {1: Chunk('moving/VP-1'), 2: Chunk('see/VP-2')}
sentence.relations["SBJ"]
    {2: Chunk('we/NP-SBJ-2')}
sentence.relations["OBJ"]
    {1: Chunk('vehicle/NP-OBJ-1'), 2: Chunk('a series/NP-OBJ-2')}
sentence.relations["OBJ"].keys()
    [1, 2]
sentence.relations["SBJ"].keys()
    [2]

print(sentence.relations["SBJ"].keys(),sentence.relations["OBJ"].keys(),sentence.relations["VP"].keys())
    ([2], [1, 2], [1, 2])
print max(sentence.relations["SBJ"].keys(),sentence.relations["OBJ"].keys(),sentence.relations["VP"].keys())
    [2]


-- 1,037,070
select *
from chunktbl c;

-- 7,958,249
select *
from sentenceTBL;

select c.fileseq, f.fileName, f.genre, c.sentseq, s.sentence, c.pos, c.neg, c.neu, c.com, c.id, c.sbj, c.vp, c.obj
from chunkTBL c,  sentenceTBL s, fileTBL f
where c.fileSeq = s.fileSeq
and c.sentSeq = s.seq
and s.fileSeq = f.seq
order by s.fileseq, c.sentseq, c.id;

select s.fileseq, s.seq, s.sentence, c.id, c.pos, c.neg, c.neu, c.com, c.sbj, c.vp, c.obj
from sentenceTBL s LEFT JOIN chunkTBL c  ON s.fileSeq=c.fileSeq and s.seq=c.sentSeq
order by s.fileseq, s.seq, c.id;

select * from chunktbl where fileseq=2381 and sentseq=1033;
-- 5052
select * from filetbl ;

select *
from sentenceTBL s, fileTBL f
where f.seq = s.fileSeq;