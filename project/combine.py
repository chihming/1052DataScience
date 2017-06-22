from collections import defaultdict
from math import log
import os, sys

pairs_file = './exp/test.pairs'
feature_file = sys.argv[1]
prediction_file = sys.argv[2]

#print ('load pairs')
user_list = []
title_list = []
answer_list = []
with open(pairs_file) as f:
    for line in f:
        answer, user, title = line.rstrip().split(' ')
        answer_list.append(float(answer))
        user_list.append(user)
        title_list.append(title)

#print ('load features')
prediction_list = []
with open(feature_file) as f:
    for line in f:
        features = list(map(float, line.rstrip().split()))
        
        score = 0.
        time_diff = features[0]
        pop = log(features[1])/10.
        last_watched1 = features[2]
        last_watched3 = features[3]
        last_watched5 = features[4]
        last_coappear1 = features[5]
        last_coappear3 = features[6]
        last_coappear5 = features[7]
        all_coappear1 = features[8]
        all_coappear3 = features[9]
        all_coappear5 = features[10]
        most_coappear0 = features[11]
        most_coappear1 = features[12]
        most_coappear3 = features[13]
        most_coappear5 = features[14]
        total_times = features[15]
        watch_times = features[16]
      
        score += pop
        score += last_watched1
        if time_diff <= 4:
            score += (last_watched3-last_watched1)*0.5
            score += (last_watched5-last_watched3)*0.25
            score += last_coappear1*4.
            score += most_coappear0*.5
        elif time_diff <= 42:
            score += (last_watched3-last_watched1)*0.5
            score += all_coappear5*1.
        else:
            score += all_coappear5*3.

        prediction_list.append( score )

#print ('prepare predictions/answers')
answers = {}
predictions = defaultdict(dict)
for uid, tid, ans, pred in zip(user_list, title_list, answer_list, prediction_list):
    predictions[uid][tid] = pred
    if ans == 1.:
        answers[uid] = tid

#print ('evaluating')
matched = 0.
matched2 = 0.
print ('user_id,title_id')
for uid in predictions:
    first_title = sorted(predictions[uid], key=predictions[uid].get, reverse=True)[0]
    print ("%s,%s" % (uid, first_title))
    #if first_title == answers[uid]:
    #    matched += 1.
    #seond_title = sorted(predictions[uid], key=predictions[uid].get, reverse=True)[1]
    #if seond_title == answers[uid]:
    #    matched2 += 1.

#print ('cv:', matched/len(predictions))
#print ('cv:', (matched+matched2)/len(predictions))

