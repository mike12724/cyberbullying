import numpy as np
import cPickle as pickle
from sklearn import svm
from sklearn.externals import joblib
from scipy.sparse import csr_matrix,vstack,save_npz
import random

finalMat = None
devMat = None
testMat = None
labels = []
devLabels = []
testLabels = []
features = []

with open('feature_list.txt','rb') as f:
    features = pickle.load(f)
numFeat = len(features)

with open('training_labels.txt','rb') as f:
    labels = pickle.load(f)
numExamples = len(labels) #number of training examples

with open('training_matrix.txt','rb') as f:
    data = pickle.load(f)
    
i = 0
for line in data: #each line is a row
    rowAr = [0 for j in range(len(line))]
    a = csr_matrix((np.ones(len(line)),(rowAr,line)),shape = (1,numFeat))
    if i < numExamples*.75: #60% of all data for training
        if finalMat == None: finalMat = a
        else: finalMat = vstack([finalMat,a])
    else: #20% train-dev
        if devMat == None: devMat = a
        else: devMat = vstack([devMat,a])
        
    i+=1
    if i%100 == 0:
        print i

trainLabels = labels[0:int(numExamples*.75)+1]
devLabels = labels[int(numExamples*.75)+1:]

clf = svm.NuSVC(.05,probability = True) 
clf.fit(finalMat,trainLabels)#magic happens
    
a = clf.predict(devMat)
wrong = 0
missed_bully = 0
for i in range(len(devLabels)):    
    if a[i] - devLabels[i] != 0:#wrong prediction
        wrong += 1
    if a[i] == 0 and devLabels[i] == 1: #missed a bullying incidence
        missed_bully += 1
print 'Fraction of wrong guesses on dev set: ' + str(float(wrong)/len(devLabels))
print 'Fraction of missed bullying on dev set: ' + str(float(missed_bully)/len(devLabels))


with open('test_labels.txt') as f:
    testLabels = pickle.load(f)

with open('test_matrix.txt') as f:
    data = pickle.load(f)

print "Creating test matrix"
i = 0
for line in data: #each line is a row
    rowAr = [0 for j in range(len(line))]
    a = csr_matrix((np.ones(len(line)),(rowAr,line)),shape = (1,numFeat))
    if testMat == None: testMat = a
    else: testMat = vstack([testMat,a])       
    i+=1
    if i%100 == 0:
        print i

a = clf.predict(testMat)
wrong = 0
missed_bully = 0
for i in range(len(testLabels)):    
    if a[i] - testLabels[i] != 0:#wrong prediction
        wrong += 1
    if a[i] == 0 and testLabels[i] == 1: #missed a bullying incidence
        missed_bully += 1
print 'Fraction of wrong guesses on test set: ' + str(float(wrong)/len(testLabels))
print 'Fraction of missed bullying on test set: ' + str(float(missed_bully)/len(testLabels))


#Final SVM update for simulator
ultraFinal= vstack([finalMat,devMat,testMat])
finalLabels = trainLabels + devLabels + testLabels
clf = svm.NuSVC(.05,probability = True) 
clf.fit(ultraFinal,finalLabels)
joblib.dump(clf,'model.pkl')
save_npz('master_convo.npz',ultraFinal) #for updating during simulation
with open('master_labels.txt','wb') as f:
    pickle.dump(finalLabels,f)

