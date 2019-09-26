#NLP Assignment 2 - September, 2019
# -*- coding: utf-8 -*-
import io
import re, sys
import os
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from math import log, pow
#from sklearn.feature_extraction.text import CountVectorizer

"""variables for positive words"""
ngramcounterpos = 0 #keeps track of the number of unique results we get, given an n-gram.
allPoswords = [] #keeps track of all words in the positive list
normalizedPoswords = [] #all postive words after they have been normalized.
vocabularypos = [] #the vocabulary of positive words
positiveProb = {} #a dictionary of words as the key and their probability of being positive as the value.
directory = "/Users/priscillaikhena/Downloads/movies/pos/"
realnormalizedposwords = []


"""variables for negative words"""
directoryneg = "/Users/priscillaikhena/Downloads/movies/neg/"
ngramcounterneg = 0
allNegWords = []
vocabularyneg = []
normalizedNegwords = []
negativeProb = {} #a dictionary of words as the key and their probability of being positive as the value.
realnormalizednegwords = []

"""Opening both positive and negative files, and then normalizing the words in them"""

#Opens the positive file folder, and loops through the positive reviews.
for filename in os.listdir(directory):
    with io.open(os.path.join(directory, filename), "r", encoding='utf-8') as bookFile:
        wordList = bookFile.readlines()

        for i in wordList:
            match = re.split(r'\W+', i)

            for word in match:
                allPoswords.append(word)

            n = 1
            sixgrams = ngrams(match, n)

            for grams in sixgrams:
                    ngramcounterpos = ngramcounterpos + 1

#Opens the negative file folder, and loops through the positive reviews.
for filename in os.listdir(directoryneg):
    with io.open(os.path.join(directoryneg, filename), "r", encoding='utf-8') as bookFileNeg:
        wordListNeg = bookFileNeg.readlines()

        for i in wordListNeg:
            match = re.split(r'\W+', i)

            for word in match:
                allNegWords.append(word)

            m = 1
            allgrams = ngrams(match, m)

            for grams in allgrams:
                    ngramcounterneg = ngramcounterneg + 1

# Lowering Words in the word arrays of both negative and positive words. This is part of the normalization process

def lower(word):
    word = word.lower()
    return word

for word in allPoswords:
    newword = lower(word)
    normalizedPoswords.append(newword)

for word in allNegWords:
    newword = lower(word)
    normalizedNegwords.append(newword)

"""Building the vocabulary, and creating the model by calculating probabilities"""


def calculateProbScore(wordfreqinpos, sentimentvocab, numberofvocab, k):

    score = log((wordfreqinpos + k), 10) / log((sentimentvocab + (numberofvocab * k)), 10)
    return score

normalizedPoswordsCount = Counter(normalizedPoswords)
normalizedNegwordsCount = Counter(normalizedNegwords)

for key, value in normalizedPoswordsCount.iteritems():

        realnormalizedposwords.append(key) #getting distinct positive words here
        #print 'this is key %s' % key
        if value >= 25:
            vocabularypos.append(key)
            posscore = calculateProbScore(value, 369, 680, 1)
            positiveProb[key] = posscore

for key, value in normalizedNegwordsCount.iteritems():

        realnormalizednegwords.append(key) #getting distinct negative words here
        if value >= 25:
            vocabularyneg.append(key)
            negscore = calculateProbScore(value, 342, 680, 1)
            negativeProb[key] = negscore


"""Testing the model"""

directorytest = "/Users/priscillaikhena/Downloads/movies/test/"

allTestWords = []
normalizedTestWords = []
realnormalizedTestWords = []
normalizedTestWordsCount = []
textfiles = []

for i in range(51):
    allTestWords.append([])
    normalizedTestWords.append([])
    realnormalizedTestWords.append([])
    normalizedTestWordsCount.append([])


#Function to open the test file, loop through and normalize the words.
def openAndNormalize():
    j = 0

#Opens the test file folder, and loops through the text files.
    for testfilename in os.listdir(directorytest):
        textfiles.append(testfilename)

        with io.open(os.path.join(directorytest, testfilename), "r", encoding='utf-8') as bookFileTest:

            wordListTest = bookFileTest.readlines()

            for i in wordListTest:
                match = re.split(r'\W+', i)

                for word in match:

                    allTestWords[j].append(word)
                    newtestword = lower(word)
                    normalizedTestWords[j].append(newtestword)


        j = j + 1


openAndNormalize()

#removing duplicates in the normalized test words.
for l in range(0, 50):

    normalizedTestWordsCount[l] = Counter(normalizedTestWords[l])


for k in range(0, 50):
    for key, value in normalizedTestWordsCount[k].iteritems():
        realnormalizedTestWords[k].append(key) #this list of list now doesn't contain duplicates.

#Function to get the probability that a given word is positive

def checkWordProbPos(word):
    if word in positiveProb.keys():
        posvalue = positiveProb.get(word)

    else:
        posvalue = 0

    return posvalue


#Function to get the probability that a given word is negative
def checkWordProbNeg(word):
    if word in negativeProb.keys():
        posvalue = negativeProb.get(word)

    else:
        posvalue = 0

    return posvalue

#Function to loop through the words in a review, checking the product of positve probabilities against the product of negative word probabilities.
#And then select the higher product result as the nature of the sentence. It returns the detected nature.
resultList = []
def checkReview():
    i = 0
    for list in realnormalizedTestWords:


        sumpos = []
        sumneg = []
        for word in realnormalizedTestWords[i]:
            #print 'this is i %s' % i
            #print 'this is the word %s' % word
            wordposvalue = checkWordProbPos(word)
            sumpos.append(wordposvalue)
            #print 'this is the positve prob %s' % wordposvalue
            wordnegvalue = checkWordProbNeg(word)
            sumneg.append(wordnegvalue)
            #print 'this is the negative prob %s' % wordnegvalue



        #Here we add, all the values in the positive and negative arrays, and then compare them to each other.
        sumposvalue = 0
        for num in sumpos:
            sumposvalue += num

        sumnegvalue = 0
        for num in sumneg:
            sumnegvalue += num
        print i
        print sumposvalue
        print sumnegvalue
        if sumposvalue > sumnegvalue:
            resultList.append('P')

        if sumposvalue < sumnegvalue:
            resultList.append('N')



        i = i + 1


checkReview()

#Printing out results to compare
accuracy = 0
for q in range(0, 50):

    if textfiles[q].startswith('P') == resultList[q].startswith('P'):
        accuracy = accuracy + 1

    elif textfiles[q].startswith('N') == resultList[q].startswith('N'):
        accuracy = accuracy + 1

    print textfiles[q]
    print resultList[q]

print accuracy

