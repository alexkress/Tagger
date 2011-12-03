import re
import string

#works something like if evaluation(c, r): get_stats(); push_to_db(); 

c = "///He. drove. the. car." 
r = "pn v pn n" 

def evaluation(call, resp):

    #assuming they aren't labeling punctuation
    call = call.translate(string.maketrans("",""), string.punctuation)

    call_ = re.split(' ', call)
    resp_ = re.split(' ', resp)

    #these could be something else..
    pos = ['n', 'pn', 'aj', 'v', 'av', 'pr', 'c', 'in']

    if len(call_) != len(resp_):
        print("Call and response have different number of tokens")
        return False

    if not all(r in pos for r in resp_):
        print("Invalid tokens in response")
        return False

    #push the values into database? here or later...
    #check stats
    
    return True

def stats(call_l, resp_l):

    #check each tag against call token in db  

    pass

if __name__ == '__main__':
    evaluation(c, r)
