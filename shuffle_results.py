import random
import cPickle as pickle
#shuffle our examples, separate into train and test

labels = []
with open('labels.txt','rb') as f:
    labels = pickle.load(f)
numExamples = len(labels)
with open('feature_matrix.txt','rb') as f:
    data = pickle.load(f)
c = list(zip(data,labels))
random.shuffle(c)
data, labels = zip(*c)
train_label = labels[0:int(0.8*numExamples)]
test_label = labels[int(0.8*numExamples):]
train_data = data[0:int(0.8*numExamples)]
test_data = data[int(0.8*numExamples):]

with open('test_labels.txt','wb') as f:
    pickle.dump(test_label,f)
with open('test_matrix.txt','wb') as f:
    pickle.dump(test_data,f)
with open('training_labels.txt','wb') as f:
    pickle.dump(train_label,f)
with open('training_matrix.txt','wb') as f:
    pickle.dump(train_data,f)
