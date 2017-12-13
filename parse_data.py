import glob
import string
import cPickle as pickle
import time
from scipy.sparse import csr_matrix,vstack
#from autocorrect import spell
#label_packet Packet1Concensus

n = 1 #num chars/words
w = 1 #chars or words

using_files = []
labels = []
featureSet = set() #initial unique feature storage
featureList = [] #For features matrix
features = [[]] #Actual feature matrix
filt = set(string.printable)

def feature_list_extractor(filename,n,w):
    #Attempt 1: 3-gram character extractor
    #Attempt 2: 2-gram character extractor
    #Attempt 3: 4-gram character extractor
    #Attempt 4: 2-gram word extractor
    #Attempt 5: 1-gram word extractor
    #Attempt 6: TODO try 3-gram char again
    with open(filename) as data_file:
        info = data_file.readlines()
        if len(info) == 0:
            return 0
        else:
            for item in info:
                if '<body>' in item:
                    a = item[7:] #remove <body>, punctuation, undesirables
                    a = a.translate(None,string.punctuation)
                    a = filter(lambda x: x in filt, a)
                    if w:
                        a = a.lower().split()
                        b = [' '.join(a[i:i+n]) for i in range(len(a)-n+1)]
                    else:
                        a= ''.join(item.split()) #Removes spaces
                        b = [a[i:i+n] for i in range(len(a)-n+1)]
                    for gram in b:
                        if len(gram) > 15:
                            continue
                        #This is the slow spell-check code
                        #gram = spell(gram)

                        featureSet.add(gram)
            return 1

def feature_extractor(filename,n,w):
    #populate the features matrix
    with open(filename) as data_file:
        l = []
        for item in data_file:
            if '<body>' in item:
                a = item[7:] #remove 'body, punctuation, undesirable chars'
                a = a.translate(None,string.punctuation)
                a = filter(lambda x: x in filt, a)
                if w:
                    a = a.lower().split()
                    b = [' '.join(a[i:i+n]) for i in range(len(a)-n+1)]
                else:
                    a= ''.join(item.split()) #Removes spaces
                    b = [a[i:i+n] for i in range(len(a)-n+1)]
                for word in b:
                    if len(word) > 15:
                        continue
                    #todo: put in later
                    #word = spell(word)
                    l.append(featureList.index(word)) #efficient storage
        features.append(l)

def parse_data(n,w):
    blabels = glob.glob('Myspace\\Bully output\\*')
    for lbl in blabels:
        print lbl
        with open(lbl) as label_file:
            for i,line in enumerate(label_file):
                s = line.split(',')
                if i == 0: #Funky csv chars
                    s[0] = s[0][3:]                   
                if feature_list_extractor('Myspace\\' + s[0] + '.xml',n,w):
                    using_files.append('Myspace\\' + s[0] + '.xml')
                else:
                    continue               
                if s[1] == 'N':
                    labels.append(0)
                else:
                    labels.append(1)

    
def createMatrix(n,w):
    global features
    i = 0
    for line in using_files:
        i += 1
        if i%100 == 0: print i
##        if i%1000 == 0:
##            with open('feature_matrix.txt','ab') as f:
##                pickle.dump(features,f)
##            features = [[]] #clear for memory
        feature_extractor(line,n,w)
    with open('feature_matrix.txt','ab') as f:
        pickle.dump(features,f)

    
#CODE STARTS HERE

t = time.time()
parse_data(n,w)
featureList = list(featureSet)

#Save items                
with open('using_files.txt','wb') as f:
    pickle.dump(using_files,f)
with open('feature_list.txt','wb') as f:
    pickle.dump(featureList,f)
with open('labels.txt','wb') as f:
    pickle.dump(labels,f)

createMatrix(n,w)
time_elapsed = time.time()-t
print time_elapsed
