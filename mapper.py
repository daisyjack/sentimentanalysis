#! /usr/bin/env python
# coding: utf-8
import sys
import jieba
import logging
from jieba import posseg as pseg
import json
#from smallseg import SEG
#seg = SEG()
reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(level=logging.INFO)
class WordPos(object):
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos
    def __str__(self):
        return self.word + '/' + self.pos
def loadDict(fileName, score):
    wordDict = {}
    with open(fileName) as fin:
        for line in fin:
            line = line.decode('utf-8')
            word = line.strip()
            #logging.info(word.decode('utf-8'))
            wordDict[word] = score
    return wordDict

def appendDict(wordDict, fileName, score):
    with open(fileName) as fin:
        for line in fin:
            line = line.decode('utf-8')
            word = line.strip()
            wordDict[word] = score

def loadExtentDict(fileName):
    extentDict = {}
    for i in range(6):
        with open(fileName + str(i + 1) + ".txt") as fin :
            for line in fin:
                line = line.decode('utf-8')
                word = line.strip()
                extentDict[word] = i + 1
    return extentDict
unicode_str = unicode('中文', encoding='utf-8')
print unicode_str
logging.info('我是水'.decode('utf-8'))
#postDict = loadDict("sentimentDict/正面情感词语（中文）.txt".decode('utf-8'), 1)
postDict = loadDict("sentimentDict/positive.txt".decode('utf-8'), 1)
#print postDict
# appendDict(postDict, u"sentimentDict/正面评价词语（中文）.txt", 1)
# appendDict(postDict, u"sentimentDict/正面评价词语（中文）1.txt", 1)
# appendDict(postDict, u"sentimentDict/正面评价词语（中文）2.txt", 1)
#negDict = loadDict(u"sentimentDict/负面情感词语（中文）.txt", -1)
negDict = loadDict(u"sentimentDict/negative.txt", -1)
#print negDict
#appendDict(negDict, u"sentimentDict/负面评价词语（中文）.txt", -1)
extentDict = loadExtentDict(u"sentimentDict/程度级别词语（中文）")
inverseDict = loadDict(u"sentimentDict/否定词语.txt", -1)
punc = loadDict(u"sentimentDict/标点符号.txt", 1)
stop = loadDict(u'sentimentDict/stopword.txt', 1)
exclamation = {"!":2, "！":2}
sentiment_pos = ['n', 'v', 'a', 'i', 'j', 'l', 'o', 'z', 'zg']
logging.info('load finished')
for line in ['e']:
    line = line.strip()
    #record = json.loads(line[1:-1])
    #key = record["weiboId"]
    #content = record["content"]
    #wordList = seg.cut(content)
    #wordList.reverse()
    content = u'【NASA 发言人：美国当年登月成功耗资 250 亿美元】 -嫦娥三号发射成功，直奔月球而去。此前，全世界仅有美国、' \
              u'前苏联成功实施了 13 次无人月球表面软着陆，而中国也即将有望成为第 3 个实现月球软着陆的国家。'
    seg_list = pseg.cut(content)
    wordList = []
    #wordList = list(seg_list)
    for word, pos in seg_list:
        wordList.append(WordPos(word, pos))
    lastWordPos = 0
    lastPuncPos = 0
    i = 0
    posTotal = 0
    negTotal = 0
    for word_pos in wordList:
        word = word_pos.word
        pos = word_pos.pos
        print word_pos.word + '/' + word_pos.pos,
        if word in punc:
            lastPuncPos = i
            print 'punc'
        # elif word in stop:
        #     print 'stop'
        elif word in postDict and (pos[0] in sentiment_pos):
            print 'post',
            if lastWordPos > lastPuncPos:
                start = lastWordPos
            else:
                start = lastPuncPos
            score = 1
            #print "start: " + str(start)
            #print "end: " + str(i)
            for word_pos_before in wordList[start+1:i]:
                word_before = word_pos_before.word
                if word_before in extentDict:
                    score = score * extentDict[word_before]
                if word_before in inverseDict:
                    score = score * -1
            for word_pos_after in wordList[i+1:]:
                word_after = word_pos_after.word
                if word_after in punc:
                    if word_after in exclamation:
                        score = score + 2
                    else:
                        break
            #print '%s\t%s\t%s' % (key, word, score)
            print '%s\t%s' % ('pp', score)
            lastWordPos = i
            if score > 0:
                posTotal += score
            else:
                negTotal += score
        elif word in negDict and (pos[0] in sentiment_pos):
            print 'neg',
            if lastWordPos > lastPuncPos:
                start = lastWordPos
            else:
                start = lastPuncPos
            score = -1
            #print "start: " + str(start)
            #print "end: " + str(i)
            for word_pos_before in wordList[start+1:i]:
                word_before = word_pos_before.word
                if word_before in extentDict:
                    score = score * extentDict[word_before]
                if word_before in inverseDict:
                    score = score * -1
            for word_pos_after in wordList[i+1:]:
                word_after = word_pos_after.word
                if word_after in punc:
                    if word_after in exclamation:
                        score = score - 2
                    else:
                        break
            #print '%s\t%s\t%s' % (key, word, score)
            print '%s\t%s' % ('nn', score)
            lastWordPos = i
            if score > 0:
                posTotal += score
            else:
                negTotal += score
        i = i + 1
    print '正分数'.decode('utf-8'),posTotal,'负分数'.decode('utf-8'),negTotal



