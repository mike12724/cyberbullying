# cyberbullying
CS229 Final Project
All files provided and ready to run simulator.py
Read step 4 for simulator use

If you wish to recreate the experiment from scratch, do the following:

0. Delete all non-py files from the main directory (files, not folders) 

1. Edit parse_data.py
You will find 2 hyperparameters
	- w = boolean indicating word or character gram
	- n = number of variable in each dictionary slot
	- default: 1 and 1

1.5 Run parse_data
	Requires a folder titled "Myspace" in the same folder as parse_data
	Requires a folder titled "Bully output" inside "Myspace", containing files like the sample one provided
	Requires XML files of conversations inside "Myspace"
	Outputs as pickle dumps:
		using_files.txt - which XML conversation files were used
		feature_list.txt - feature dictionary
		labels.txt - labels aligned with using_files
		feature_matrix.txt -  contains sentence vectors, encoded using feature_list

2. Run shuffle_results.py
	Outputs as pickle dumps:
		training/test_labels.txt: Shuffled 80-20 division of labels.txt
		training/test_matrix.txt: Shuffled (same) 80-20 division of feature_matrix.txt

3. Run svm.py
	Trains SVM using training data (which is divided 80-20 into train/dev)
	Outputs error on dev set
	Outputs error on test set

4. Run simulator.py
	Do NOT run from IDLE (Windows), just double click
	Simulator is extremely basic; input text and press enter
	If bullying is detected, it will output as such
	type "s bully" (no quotes) to tell the SVM the previous statement was bullying
	same for "s not bully"
	SVM will NOT update until you type "Done"
	Outputs:
		master_convo.npz - sparse matrix representation of ALL data, direct SVM input
		model.pkl - Current SVM model

5. Re-run simulator.py to test
		

Enjoy!
