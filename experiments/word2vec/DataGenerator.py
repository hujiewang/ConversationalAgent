__author__ = 'Hujie Wang'

import json
import re
import keras.preprocessing.text as T
from tqdm import tqdm
import time
import os

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
FOUT_PATH="./data/data_generated"
SELECTED_SUBREDDIT=[]
number_of_tokens=0
number_of_comments=0
last_number_of_comments=0
start_time=None
class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            generate(obj)
        return None

def do(fname, subreddit=[]):
        '''
        :param fname(Reddit comment JSON file)
        :      subreddit(a list of subreddit names)
        :return a dict of JSON object:
        '''
        global start_time
        global number_of_tokens
        global number_of_comments
        global last_number_of_comments
        global FOUT_PATH
        global SELECTED_SUBREDDIT
        start_time = time.time()
        number_of_tokens=0
        number_of_comments=0
        last_number_of_comments=0
        SELECTED_SUBREDDIT=subreddit
        print('Converting reddit comments into tokens...')
        with open(fname) as data_file:
            data = json.loads(data_file.read(),cls=ConcatJSONDecoder)
        print('Data generation completed!')
        print('Number of comments:'+str(number_of_comments))
        print('Number of tokens:'+str(number_of_tokens))

def getString(obj):
        '''
        Return a list of strings given a JSON data

        :param data (JSON)
        :return: a list of strings
        '''
        global number_of_comments
        global start_time
        global last_number_of_comments
        number_of_comments+=1
        current_time=time.time()
        #duration=int((current_time - start_time)*1000)
        if number_of_comments%100000==0:
            print(number_of_comments)
            #print(repr((number_of_comments-last_number_of_comments)/duration )+" comments per second" )
            #last_number_of_comments=number_of_comments
        return obj['body']

def string2sentences(str):
        '''
        :param str:
        :return a list of sentences:
        '''
        return list(filter(bool,re.split(r'[;,.!?]+',str)))


def write(fname,sequences):
        '''
        Append list of tokens into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''
        with open(fname,'ab') as fout:
            for i in range(len(sequences)):
                #for j in range(len(sequences[i])):
                fout.write(bytes(sequences[i], 'UTF-8'))
                if i!=len(sequences)-1:
                    fout.write(bytes(' ', 'UTF-8'))
                else:
                    fout.write(bytes('\n', 'UTF-8'))

def text2sequence(text):
        '''
        Convert a string into a list of words, filtering punctuations and irreverent symbols
        :param text(a sttring):
        :return a list of words:
        '''
        global number_of_tokens
        sequence = T.text_to_word_sequence(text, filters=T.base_filter(), lower=True, split=" ")
        for i in range(len(sequence)):
            sequence[i]=re.sub(r'^[0-9]+$','<NUMBER>',sequence[i])
            number_of_tokens+=1
        return sequence

def generate(obj):
    if obj['subreddit'] in SELECTED_SUBREDDIT or not SELECTED_SUBREDDIT:
        sequences=[]
        global number_of_tokens
        number_of_tokens+=1
        sentences=string2sentences(getString(obj))
        for sentence in sentences:
            #sequences.append(text2sequence(sentence))
            sequences += text2sequence(sentence)
        if not SELECTED_SUBREDDIT:
            write(FOUT_PATH, sequences)
        else:
            party = obj['subreddit']
            write('./data/'+party+'.sub', sequences)
            with open('./data/'+party+'.aut', 'a') as author:
                author.write(obj['author'])
                author.write('\n')

