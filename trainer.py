__package__ = "typeIt"

import pandas as pd
import re
import datetime
import sklearn.feature_extraction
import sklearn.svm
import pickle
import sys

def train(prefix):
    print("creating classifier for " + prefix)
    print("open data")
    with open(prefix + "all_data.p",'rb') as db_file:
        all_data = list(pickle.load(db_file))
    print("open lables")
    with open(prefix + "all_lables.p",'rb') as db_file:
        lables = list(pickle.load(db_file))
    print("creating vectorizer")
    vec = sklearn.feature_extraction.DictVectorizer()
    vec.fit_transform(all_data)
    print("vectorizing data")
    testing = vec.transform(all_data)
    print("num of samples: " + str(len(all_data)))
    algorithms = sklearn.svm.LinearSVC()
    algorithms.fit(testing,lables)
    print("created classifier, saving to pickle")
    with open(prefix + "classifier.p", "wb") as newfile:
        pickle.dump(algorithms, newfile)
    with open(prefix + "vectorizer.p", "wb") as newfile:
        pickle.dump(vec, newfile)
    print("done saving")

def test(prefix):

    print("testing for: " + prefix)

    with open(prefix + "training_data.p",'rb') as db_file:
        training_data = list(pickle.load(db_file))
    with open(prefix + "training_lables.p",'rb') as db_file:
        training_lables = list(pickle.load(db_file))
    with open(prefix + "testing_data.p",'rb') as db_file:
        testing_data = list(pickle.load(db_file))
    with open(prefix + "testing_lables.p",'rb') as db_file:
        testing_lables = list(pickle.load(db_file))
    with open(prefix + "all_data.p",'rb') as db_file:
        all_data = list(pickle.load(db_file))
    with open(prefix + "classes_dict.p", 'rb') as classes_file:
        contacts = pickle.load(classes_file)


    print("SVC with linear kernel")
    a = len(training_data)
    b = len(training_lables)
    c = len(testing_data)
    d = len(testing_lables)
    vec = sklearn.feature_extraction.DictVectorizer()
    vec.fit_transform(all_data)
    training = vec.transform(training_data)
    algorithms = sklearn.svm.SVC(kernel="linear")
    algorithms.fit(training,training_lables)
    print("training")
    total = len(training_lables);
    correct = 0
    for i in range(total):
        if training_lables[i] == algorithms.predict(training.getrow(i)):
            correct += 1
    print_resutls(correct, total)

    print("testing")
    testing = vec.transform(testing_data)
    total = len(testing_lables);
    correct = 0
    for i in range(total):
        if testing_lables[i] == algorithms.predict(testing.getrow(i)):
            correct += 1
    print_resutls(correct, total)

    print("LinearSVC")
    algorithms = sklearn.svm.LinearSVC(dual=False)
    algorithms.fit(training,training_lables)
    print("training")
    total = len(training_lables);
    correct = 0
    for i in range(total):
        if training_lables[i] == algorithms.predict(training.getrow(i)):
            correct += 1
    print_resutls(correct, total)

    print("testing")
    testing = vec.transform(testing_data)
    total = len(testing_lables);
    correct = 0
    for i in range(total):
        guess = algorithms.predict(testing.getrow(i))
        # print(contacts[guess[0]] + "\t\t\t" + contacts[testing_lables[i]],end="\t\t\t")
        if testing_lables[i] == guess:
            correct += 1
    print_resutls(correct, total)

    with open(prefix + "classifier.p", "wb") as newfile:
        pickle.dump(algorithms, newfile)
    with open(prefix + "vectorizer.p", "wb") as newfile:
        pickle.dump(vec, newfile)

def re_train(msg, label):
    pass

def print_resutls(correct, total):
    print(str(correct) + " correct out of " + str(total) + " samples ("+str(int(correct/total*1000)/10)+"%)\n")


def execute_command(method, prefix):
    prefix = "./static/data/" + prefix + "_"
    if method == "train":
        train(prefix)
    elif method == "test":
        test(prefix)
    else:
        raise 0

if __name__ == "__main__":
    args = sys.argv
    with open("./static/data/user_ids.p", "rb") as uidfile:
        users_dict = dict(pickle.load(uidfile))
    try:
        if len(args) > 1:
            method = args[1]
            if len(args) == 2:
                method = args[1]
                for uid in users_dict.keys():
                    execute_command(method, users_dict[uid][1])
            if len(args) == 3:
                uid = int(args[2])
                execute_command(method, users_dict[uid][1])
            else:
                raise 0
        else:
            raise 0
    except:
        print("usage: python trainer.py <method name (train, test)> [<user id>]")