import re
import string
import csv
import numpy as np

#works something like:
#if evaluation(c, r): get_stats(); push_to_db(); 

c = "///He. drove. the. car." 
r = "pn v pn n" 

class Evaluator(object):

    def __init__(self):
        self.pos = ['n', 'pn', 'aj', 'v', 'av', 'pr', 'c', 'in', 'u']
        self.lookup = dict(zip(self.pos, ['noun', 'pronoun', 'adjective', 'verb', 'adverb', 'preposition', 'conjunction', 'interjection', 'unknown']))  

    def evaluation(self, call, resp):

        #assuming they aren't labeling punctuation
        call = call.translate(string.maketrans("",""), string.punctuation)

        #group spaced elements
        call_ = re.split(' ', call)
        resp_ = re.split(' ', resp)

        #check if there are the same number of tokens
        if len(call_) != len(resp_):
            print("Call and response have different number of tokens")
            return False

        #check there are invalid tokens
        if not all(r in self.pos for r in resp_):
            print("Invalid tokens in response")
            return False

        self.tags = resp_
        return True

    def push(self, filename, sentenceID, workerID):
        f = open(filename, 'a')
        f.write('%i; %i; %s\n'%(sentenceID, workerID, str(self.tags))) 
        f.close()

class Stats(object):

    def __init__(self):
        self.pos = ['n', 'pn', 'aj', 'v', 'av', 'pr', 'c', 'in', 'u']
        self.posID = dict(zip(self.pos, range(len(self.pos))))
        self.lookup = dict(zip(self.pos, ['noun', 'pronoun', 'adjective', 'verb', 'adverb', 'preposition', 'conjunction', 'interjection', 'unknown']))
        self.dtype = [('Word', 'S50'), ('SentenceID', int), ('WorkerID', int), ('POSID', int)]
        
    def format(self, sentenceList, filename):
        a = csv.reader(open('%s'%filename, 'rb'), delimiter=';')
        sentences = dict()
        f  = open('%s'%sentenceList, 'rb')

        for i, line in enumerate(f.readlines()):
            line = line.strip()
            line = line[1:line.find('#')]
            line = line.split('@,')[1]
            sentences[i] = line[1:]

        count = sum([len(eval(line[2])) for line in a])
        self.data = np.zeros(count, dtype=self.dtype)
        a = csv.reader(open('%s'%filename, 'rb'), delimiter=';')
        i = 0
        print(sentences)
        for line in a:
            for k, p in enumerate(eval(line[2])):
                self.data[i]['SentenceID'] = line[0]
                self.data[i]['WorkerID'] = line[1]
                self.data[i]['POSID'] = self.posID[p]
                self.data[i]['Word'] = re.split(' ', sentences[eval(line[0])])[k]
                i += 1

def evaluation(call, resp):

    #assuming they aren't labeling punctuation
    call = call.translate(string.maketrans("",""), string.punctuation)

    #group spaced elements
    call_ = re.split(' ', call)
    resp_ = re.split(' ', resp)

    #these could be something else..
    pos = ['n', 'pn', 'aj', 'v', 'av', 'pr', 'c', 'in', 'u']

    #check if there are the same number of tokens
    if len(call_) != len(resp_):
        print("Call and response have different number of tokens")
        return False

    #check there are invalid tokens
    if not all(r in pos for r in resp_):
        print("Invalid tokens in response")
        return False

    #push the values into database? here or later...
    #check stats
    
    return True

if __name__ == '__main__':
    E = Evaluator()
    S = Stats()
    if E.evaluation(c, r):
        E.push('../Data/responseList.txt', 1, 1)
    S.format('../Data/sentenceList.txt','../Data/responseList.txt')
