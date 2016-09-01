__package__ = "typeIt"

import pandas as pd
import re
import datetime
import sklearn.feature_extraction
import sklearn.svm
import pickle
import typeItParser

def test_result(msg, timestamp, id):
    with open("./static/data/user_ids.p", "rb") as uid_file:
        user_dict = dict(pickle.load(uid_file))
    prefix = "./static/data/" + user_dict[int(id)][1] + "_"
    with open(prefix + "classifier.p", "rb") as newfile:
        classifier = pickle.load(newfile)
    with open(prefix + "vectorizer.p", "rb") as newfile:
        vec = pickle.load(newfile)
    with open(prefix + "classes_dict.p", "rb") as newfile:
        contacts = pickle.load(newfile)
    day_of_week, hrs = typeItParser.timestamp_to_vals(timestamp)
    msg_dict = typeItParser.parse_income_msg(msg, day_of_week, hrs)
    msg_vec = vec.transform(msg_dict)
    result = contacts[classifier.predict(msg_vec)[0]]
    return result