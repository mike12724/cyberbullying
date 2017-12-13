import numpy as np
import cPickle as pickle
from sklearn import svm
from sklearn.externals import joblib
from scipy.sparse import csr_matrix,hstack, vstack,save_npz,load_npz
import string
import random

#Note: If word not in corpus, will get added to feature list,
#but not model until next encounter in new conversation
#too complicated to directly insert

num_new_feats = 0 #counter for new words not in corpus
def feature_transformer(sentence):
    #Returns an array the svm is capable of parsing
    
    sentence = sentence.translate(None,string.punctuation) #remove puncts
    sentence = filter(lambda x: x in filt, sentence) #more pre-processing
    words = sentence.lower().split() #split into words
    l = []
    for word in words:
        if word not in features:
            features.append(word)
            global num_new_feats
            num_new_feats += 1
        else:
            l.append(features.index(word))
    rowAr = [0 for j in range(len(l))]
    return csr_matrix((np.ones(len(l)),(rowAr,l)),shape = (1,numFeat))
    
#Filter to make printable text
filt = set(string.printable)

#Load feature list
features = []
with open('feature_list.txt','rb') as f:
    features = pickle.load(f)
numFeat = len(features)

#Load up model from svm.py
clf = joblib.load('model.pkl')

#Initialize conversation storage matrix
convStore = None
labelStore = []
print 'Have a conversation with yourself!'

#Bully yourself!
prevState = None
while 1:
    statement = raw_input()
    if statement == 's bully': #svm missed bullying
        #This "if" encloses an IRL procedure unto itself, explained in report
        if convStore == None: convStore = prevState
        else: convStore = vstack([convStore,prevState])
        labelStore.append(1)
        continue
    if statement == 's not bully': #svm misclassified bullying
        if convStore == None: convStore = prevState
        else: convStore = vstack([convStore,prevState])
        labelStore.append(0)
        continue
    if statement == 'Done':
        break
    t = feature_transformer(statement)
    prediction = clf.predict_proba(t)
    if prediction[0][1] > 0.9: #margin of confidence
        print 'Extreme bullying detected!'
    elif prediction[0][1] > 0.7:
        print 'Serious bullying detected!'
    elif prediction[0][1] > 0.6:
        print 'Some bullying detected. Please moderate your language.'
    prevState = t

#Re-update SVM
labels = list(pickle.load(open('master_labels.txt','rb')))
mat = load_npz('master_convo.npz')
mat = vstack([mat, convStore])
mat = hstack([mat, csr_matrix((mat.shape[0],num_new_feats))]) #adds columns for new features
labels = labels + labelStore
clf = svm.NuSVC(.05,probability = True)

print 'Number of features added to the list: ' + str(num_new_feats)
print 'Fitting new model...'
clf.fit(mat,labels)
print 'Done'

#Redump SVM objects
joblib.dump(clf,'model.pkl')
save_npz('master_convo.npz',mat) #for updating during simulation
with open('master_labels.txt','wb') as f:
    pickle.dump(labels,f)
with open('feature_list.txt','wb') as f:
    pickle.dump(features,f)







