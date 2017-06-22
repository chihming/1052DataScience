import sys
from collections import defaultdict, Counter
from math import log
from datetime import datetime

def load_events(file_name):
    
    events = defaultdict(dict)
    with open(file_name) as f:
        next(f)
        for line in f:
            time, user, title, watch_time = line.rstrip('\n').split(',')
            events[user][title] = 1

    return events

def load_labels(file_name):
    
    labels = {}
    title_list = {}
    with open(file_name) as f:
        next(f)
        for line in f:
            user_id, title_id = line.rstrip('\n').split(',')
            labels[user_id] = title_id
            title_list[title_id] = 1
    title_list = list(title_list.keys())

    return labels, title_list


if __name__ == '__main__':

    train_file = sys.argv[1]
    label_file = './assets/labels_train.csv'
    test_file = sys.argv[2]
    
    print ('load train events')
    train_events = load_events(train_file)
    print ('load test events')
    test_events = load_events(test_file)
    print ('load train labels')
    train_labels, title_list = load_labels(label_file)
    
    train_rows = []
    test_rows = []

    for user in train_events:
        for title in title_list:
            if title in train_labels[user]:
                train_rows.append("1 %s %s" % (user, title))
            else:
                train_rows.append("0 %s %s" % (user, title))

    for user in test_events:
        for title in title_list:
            #if title in train_labels[user]:
            #    test_rows.append("1 %s %s" % (user, title))
            #else:
            test_rows.append("0 %s %s" % (user, title))

    print ('save pairs to ./exp/train.pairs')
    with open('./exp/train.pairs', 'w') as fw:
        fw.write("%s\n" % ('\n'.join(train_rows)))
    print ('save pairs to ./exp/test.pairs')
    with open('./exp/test.pairs', 'w') as fw:
        fw.write("%s\n" % ('\n'.join(test_rows)))
