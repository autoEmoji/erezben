__package__ = "typeIt"

import pandas as pd
import re
import datetime
import pickle
import sklearn
from platform import system
import sys

TIMESTAMP_REGEX = "(\d+)\/(\d+)\/(\d+)\D+(\d+):(\d+)"
DB_REGEX = TIMESTAMP_REGEX + "...([^:]+):\s([^:]+)"
DB_BEN_REGEX = "(\d+)\/(\d+)\/(\d+)\D+(\d+):(\d+):....([^:]+):\s(.*)"

MONTH, DAY, YEAR, HRS, MNS, SENDER, MESSAGE = [1, 2, 3, 4, 5, 6, 7]


def parse_income_msg(msg, day_of_week, hrs):
    msg_dict = {}
    for word in msg.split(" "):
        if word not in [" ", ""]:
            if word not in msg_dict:
                msg_dict[word] = 1
            else:
                msg_dict[word] += 1
    msg_dict["D_O_W_" + str(day_of_week)] = 1
    for i in range(-1,2):
        cur_hrs = (int(hrs) + i) % 24
        if cur_hrs < 10:
            cur_hrs = "0" + str(cur_hrs)
        msg_dict["HRS_" + str(cur_hrs)] = 1 - abs(i/2)
    return msg_dict

def create2sets(sender, prefix, num_of_contacts):
    print("creating db for: " + sender)
    if (prefix == "ben"):
        regex = DB_BEN_REGEX
    else:
        regex = DB_REGEX
    training = []
    testing = []
    trainingLable = []
    testingLable = []
    classes = {}
    added_class_name = False
    counter = 0
    for contact in range(num_of_contacts):
        added_class_name = False
        print("THIS IS CONTACT " + str(contact) + ":")
        with open("./static/data/"+prefix+"contact" + str(contact) + ".txt", "r", -1, "UTF-8") as file:
            line = file.readline()
            while line != "":
                match = re.match(regex, line)
                if match is not None:
                    if match.group(SENDER) == sender:
                        msg = match.group(MESSAGE)
                        day_of_week = datetime.date(int(match.group(YEAR)), int(match.group(MONTH)), int(match.group(DAY))).weekday()
                        hrs = match.group(HRS)
                        msg_dict = parse_income_msg(msg, day_of_week, hrs)
                        if counter % 2:
                            training.append(msg_dict)
                            trainingLable.append(contact)
                        else:
                            testing.append(msg_dict)
                            testingLable.append(contact)
                        counter += 1
                    else:
                        if not added_class_name:
                            classes[contact] = match.group(SENDER)
                            print("\t" + match.group(SENDER))
                            added_class_name = True
                line = file.readline()
    prefix = "./static/data/" + prefix + "_"
    save_to_pickle(prefix + "classes_dict.p", classes)
    save_to_pickle(prefix + "training_data.p", training)
    save_to_pickle(prefix + "training_lables.p", trainingLable)
    save_to_pickle(prefix + "testing_data.p", testing)
    save_to_pickle(prefix + "testing_lables.p", testingLable)
    print("training " + str(len(training)))
    print("testing  " + str(len(testing)))
    print("training label " + str(len(trainingLable)))
    print("testing  label " + str(len(testingLable)))
    training += testing
    trainingLable += testingLable
    print("total samples " + str(len(training)))
    print("total labels  " + str(len(trainingLable)))
    save_to_pickle(prefix + "all_data.p", training)
    save_to_pickle(prefix + "all_lables.p", trainingLable)

def timestamp_to_vals(timestamp):
    match = re.match(TIMESTAMP_REGEX, timestamp)
    hour = match.group(HRS)
    day_of_week = datetime.date(int(match.group(YEAR)), int(match.group(MONTH)), int(match.group(DAY))).weekday()
    return day_of_week, hour

def save_to_pickle(path_and_name, var):
    with open(path_and_name,'wb') as new_file:
        pickle.dump(var,new_file)

if __name__ == "__main__":
    num_of_users = 2
    arguments = {0: ["Ben", "ben", 9], 1:["Erez Levanon", "erez", 9]}
    save_to_pickle("./static/data/user_ids.p", arguments)
    if len(sys.argv) == 2:
        user_id = int(sys.argv[1])
    else:
        user_id = num_of_users
    if 0 <= user_id and user_id < num_of_users:
        arg0, arg1, arg2 = arguments[user_id]
        create2sets(arg0, arg1, arg2)
    else:
        for i in arguments.keys():
            arg0, arg1, arg2 = arguments[i]
            create2sets(arg0, arg1, arg2)

