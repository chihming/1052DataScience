import sys
from collections import defaultdict, Counter
from datetime import datetime

def load_pairs(file_name):
    
    pairs = []
    with open(file_name) as f:
        for line in f:
            answer, user, title = line.rstrip('\n').split(' ')
            pairs.append( (user, title) )

    return pairs

def load_events(file_name):
    
    events = defaultdict(dict)
    with open(file_name) as f:
        next(f)
        for line in f:
            time, user_id, title_id, watch_time = line.rstrip('\n').split(',')
            events[user_id][int(time)] = (title_id, float(watch_time))

    return events

def load_labels(file_name):
    
    labels = {}
    with open(file_name) as f:
        next(f)
        for line in f:
            user_id, title_id = line.rstrip('\n').split(',')
            labels[user_id] = title_id

    return labels

already_watched_binary = defaultdict(lambda: defaultdict(lambda: 0.))
already_watched_count = defaultdict(lambda: defaultdict(lambda: 0.))
already_watched_prob = defaultdict(lambda: defaultdict(lambda: 0.))

def get_already_watched(events):
    global already_watched_binary, already_watched_count, already_watched_prob

    for user in events:
        for time in sorted(events[user], reverse=True)[:]:
            title = events[user][time][0]
            already_watched_binary[user][title] = 1.
            already_watched_count[user][title] += 1.

    for user in already_watched_count:
        total_count = sum(already_watched_count[user].values())
        for title in already_watched_count[user]:
            already_watched_prob[user][title] = already_watched_count[user][title]/total_count


last_watch_times1 = defaultdict(lambda: defaultdict(lambda: 0.))
last_watch_times3 = defaultdict(lambda: defaultdict(lambda: 0.))
last_watch_times5 = defaultdict(lambda: defaultdict(lambda: 0.))

last_watch_coappear1 = defaultdict(lambda: defaultdict(lambda: 0.))
last_watch_coappear3 = defaultdict(lambda: defaultdict(lambda: 0.))
last_watch_coappear5 = defaultdict(lambda: defaultdict(lambda: 0.))

all_watch_coappear1 = defaultdict(lambda: defaultdict(lambda: 0.))
all_watch_coappear3 = defaultdict(lambda: defaultdict(lambda: 0.))
all_watch_coappear5 = defaultdict(lambda: defaultdict(lambda: 0.))

most_watch_coappear0 = defaultdict(lambda: defaultdict(lambda: 0.))
most_watch_coappear1 = defaultdict(lambda: defaultdict(lambda: 0.))
most_watch_coappear3 = defaultdict(lambda: defaultdict(lambda: 0.))
most_watch_coappear5 = defaultdict(lambda: defaultdict(lambda: 0.))

all_watch_times = defaultdict(lambda: 0.)
total_watch_times = defaultdict(lambda: defaultdict(lambda: 0.))

def get_last_watched(train_events, test_events, train_labels):
    global last_watch_times1, last_watch_times3, last_watch_times5
    global last_watch_coappear1, last_watch_coappear3, last_watch_coappear5
    global all_watch_coappear1, all_watch_coappear3, all_watch_coappear5
    global most_watch_coappear0, most_watch_coappear1, most_watch_coappear3, most_watch_coappear5
    global all_watch_times, total_watch_times
    
    last_coappear = defaultdict(lambda: defaultdict(lambda: 0.))
    all_coappear = defaultdict(lambda: defaultdict(lambda: 0.))
    most_coappear = defaultdict(lambda: defaultdict(lambda: 0.))
    
    for user in train_events:
        label = train_labels[user]

        watch_times = defaultdict(lambda: 0.)
        for time in sorted(train_events[user], reverse=True)[:]:
            title = train_events[user][time][0]
            watch_times[title] += 1.

        for time in sorted(train_events[user], reverse=True)[:1]:
            title = train_events[user][time][0]
            last_watch_times1[user][title] += 1.
            last_coappear[title][label] += 1

        for time in sorted(train_events[user], reverse=True)[:3]:
            title = train_events[user][time][0]
            last_watch_times3[user][title] += 1.

        for time in sorted(train_events[user], reverse=True)[:5]:
            title = train_events[user][time][0]
            last_watch_times5[user][title] += 1.

        for time in sorted(train_events[user], reverse=True)[:]:
            title = train_events[user][time][0]
            all_coappear[title][label] += 1.
    
        title = sorted(watch_times, key=watch_times.get, reverse=True)[0]
        most_coappear[title][label] += 1.

    for title in last_coappear:
        _sum = sum(last_coappear[title].values()) + 10.
        for label in last_coappear[title]:
            last_coappear[title][label] = last_coappear[title][label]/_sum

    for title in all_coappear:
        _sum = sum(all_coappear[title].values()) + 10.
        for label in all_coappear[title]:
            all_coappear[title][label] = all_coappear[title][label]/_sum

    for title in most_coappear:
        _sum = sum(most_coappear[title].values()) + 10.
        for label in most_coappear[title]:
            most_coappear[title][label] = most_coappear[title][label]/_sum

    for user in test_events:

        for time in sorted(test_events[user], reverse=True)[:1]:
            title = test_events[user][time][0]
            last_watch_times1[user][title] += 1.

        for time in sorted(test_events[user], reverse=True)[:3]:
            title = test_events[user][time][0]
            last_watch_times3[user][title] += 1.

        for time in sorted(test_events[user], reverse=True)[:5]:
            title = test_events[user][time][0]
            last_watch_times5[user][title] += 1.


    for user in test_events:
        
        watch_times = defaultdict(lambda: 0.)
        for time in sorted(test_events[user], reverse=True)[:]:
            title = test_events[user][time][0]
            watch_times[title] += 1.
            total_watch_times[user][title] += 1
            all_watch_times[user] += 1

        for time in sorted(test_events[user], reverse=True)[:1]:
            title = test_events[user][time][0]
            for label in last_coappear[title]:
                last_watch_coappear1[user][label] += last_coappear[title][label]
            for label in all_coappear[title]:
                all_watch_coappear1[user][label] += all_coappear[title][label]
            for label in most_coappear[title]:
                most_watch_coappear1[user][label] = most_coappear[title][label]

        for time in sorted(test_events[user], reverse=True)[:3]:
            title = test_events[user][time][0]
            for label in last_coappear[title]:
                last_watch_coappear3[user][label] += last_coappear[title][label]
            for label in all_coappear[title]:
                all_watch_coappear3[user][label] += all_coappear[title][label]
            for label in most_coappear[title]:
                most_watch_coappear3[user][label] = most_coappear[title][label]

        for time in sorted(test_events[user], reverse=True)[:5]:
            title = test_events[user][time][0]
            for label in last_coappear[title]:
                last_watch_coappear5[user][label] += last_coappear[title][label]
            for label in all_coappear[title]:
                all_watch_coappear5[user][label] += all_coappear[title][label]
            for label in most_coappear[title]:
                most_watch_coappear5[user][label] = most_coappear[title][label]

        title = sorted(watch_times, key=watch_times.get, reverse=True)[0]
        for label in most_coappear[title]:
            most_watch_coappear0[user][label] = most_coappear[title][label]



date_coappear = defaultdict(lambda: defaultdict(lambda: 0.))

def get_date_coappear(support_events, events, labels):
    global date_coappear
    
    end_time = datetime.fromtimestamp(1475305200)
    
    _date_coappear = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.)))

    for user in support_events:
        for time in sorted(support_events[user], reverse=True)[:3]:
            title = support_events[user][time][0]
            #if title == labels[user]: continue
            dtime = datetime.fromtimestamp(time)
            date_range = (end_time - dtime).days % 7
            _date_coappear[ date_range ][ title ][ labels[user] ] += 1.

    for _events in events:
        for user in _events:
            for time in sorted(_events[user], reverse=True)[:3]:
                title1 = _events[user][time][0]
                dtime = datetime.fromtimestamp(time)
                date_range = (end_time - dtime).days % 7
                for title2 in _date_coappear[date_range][title1]:
                    date_coappear[user][title2] += _date_coappear[date_range][title1][title2]
    
    for user in date_coappear:
        _sum = sum(date_coappear[user].values())
        for title in date_coappear[user]:
            date_coappear[user][title] = date_coappear[user][title]/_sum

coappear = defaultdict(lambda: defaultdict(lambda: 0.))
last_coappear = defaultdict(lambda: defaultdict(lambda: 0.))

def get_label_coappear(support_events, events, labels):
    global coappear, last_coappear
    
    label_coappear = defaultdict(lambda: defaultdict(lambda: 0.))
    label_last_coappear = defaultdict(lambda: defaultdict(lambda: 0.))

    for user in support_events:
        for time in sorted(support_events[user], reverse=True)[:]:
            title = support_events[user][time][0]
            if title == labels[user]: continue
            label_coappear[ title ][ labels[user] ] += 1.
        for time in sorted(support_events[user], reverse=True)[:3]:
            title = support_events[user][time][0]
            if title == labels[user]: continue
            label_last_coappear[ title ][ labels[user] ] += 1.

    for title1 in label_coappear:
        total = sum(label_coappear[title1].values())
        for title2 in label_coappear[title1]:
            label_coappear[title1][title2] = label_coappear[title1][title2]/total
    for title1 in label_last_coappear:
        total = sum(label_last_coappear[title1].values())
        for title2 in label_last_coappear[title1]:
            label_last_coappear[title1][title2] = label_last_coappear[title1][title2]/total

    for _events in events:
        for user in _events:
            for time in sorted(_events[user], reverse=True)[:3]:
                title1 = _events[user][time][0]
                for title2 in label_coappear[title1]:
                    coappear[user][title2] += label_coappear[title1][title2]
                for title2 in label_last_coappear[title1]:
                    last_coappear[user][title2] += label_last_coappear[title1][title2]


time_diff_days = defaultdict(lambda: defaultdict(lambda: 0.))

def get_time_diff(events):
    global time_diff_days
    
    end_time = datetime.fromtimestamp(1475305200)
    for user in events:
        for time in sorted(events[user], reverse=True)[:]:
            title = events[user][time][0]
            dtime = datetime.fromtimestamp(time)
            diff_days = (end_time - dtime).days
            time_diff_days[user][title] = diff_days

popularity = defaultdict(lambda: 0.)

def get_popularity(labels):
    global popularity
    
    for user in labels:
        popularity[labels[user]] += 1.


train_file = sys.argv[1]
label_file = './assets/labels_train.csv'
test_file = sys.argv[2]
train_pairs_file = sys.argv[3]
test_pairs_file = sys.argv[4]
#support_file = sys.argv[5]
#cv = int(sys.argv[3])

print ('load train events')
train_events = load_events(train_file)
print ('load test events')
test_events = load_events(test_file)
#print ('load support events')
#support_events = load_events(support_file)
print ('load train labels')
train_labels = load_labels(label_file)

#print ('load train pairs')
#train_pairs = load_pairs(train_pairs_file)
print ('load test pairs')
test_pairs = load_pairs(test_pairs_file)


print ('get time diff')
get_time_diff(train_events)
get_time_diff(test_events)

print ('dump time diff features')
test_features = []
for user, title in test_pairs:
    test_features.append("%f" % ( time_diff_days[user][title] ) )

print ('save to ./exp/time_diff.test')
with open('./exp/time_diff.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))




print ('get popularity')
get_popularity(train_labels)

print ('dump popularity features')
test_features = []
for user, title in test_pairs:
    test_features.append("%f" % ( popularity[title] ) )

print ('save to ./exp/pop.test')
with open('./exp/pop.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))





print ('get last watched')
get_last_watched(train_events, test_events, train_labels)

print ('dump last watched features')
train_features = []
test_features = []

for user, title in test_pairs:
    test_features.append("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f" % ( 
                                         last_watch_times1[user][title],
                                         last_watch_times3[user][title],
                                         last_watch_times5[user][title],
                                         last_watch_coappear1[user][title],
                                         last_watch_coappear3[user][title],
                                         last_watch_coappear5[user][title],
                                         all_watch_coappear1[user][title],
                                         all_watch_coappear3[user][title],
                                         all_watch_coappear5[user][title],
                                         most_watch_coappear0[user][title],
                                         most_watch_coappear1[user][title],
                                         most_watch_coappear3[user][title],
                                         most_watch_coappear5[user][title],
                                         all_watch_times[user],
                                         total_watch_times[user][title],
                                         ) )

print ('save to ./exp/last_watched.test')
with open('./exp/last_watched.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))

exit()
#####



print ('get date coappear')
get_date_coappear(train_events, [test_events], train_labels)

print ('dump coappear features')
train_features = []
test_features = []
for user, title in train_pairs:
    train_features.append("%f" % ( date_coappear[user][title] ) )
for user, title in test_pairs:
    test_features.append("%f" % ( date_coappear[user][title] ) )

print ('save to ./exp/date_coappear.train')
with open('./exp/date_coappear.train', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(train_features)))
print ('save to ./exp/date_coappear.test')
with open('./exp/date_coappear.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))

#exit()
#####





#exit()
#####



#exit()
#####

print ('get label coappear')
get_label_coappear(train_events, [test_events], train_labels)

print ('dump coappear features')
train_features = []
test_features = []
for user, title in train_pairs:
    train_features.append("%f %f" % ( coappear[user][title],
                                      last_coappear[user][title]) )
for user, title in test_pairs:
    test_features.append("%f %f" % ( coappear[user][title],
                                     last_coappear[user][title]) )

print ('save to ./exp/coappear.train')
with open('./exp/coappear.train', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(train_features)))
print ('save to ./exp/coappear.test')
with open('./exp/coappear.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))

#exit()
#####


print ('get already watched')
get_already_watched(train_events)
get_already_watched(test_events)

print ('dump already watched features')
train_features = []
test_features = []
for user, title in train_pairs:
    train_features.append("%f %f %f" % ( already_watched_binary[user][title],
                                         already_watched_count[user][title],
                                         already_watched_prob[user][title]
                                         ))
for user, title in test_pairs:
    test_features.append("%f %f %f" % ( already_watched_binary[user][title],
                                        already_watched_count[user][title],
                                        already_watched_prob[user][title]
                                        ))
print ('save to ./exp/already_watched.train')
with open('./exp/already_watched.train', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(train_features)))
print ('save to ./exp/already_watched.test')
with open('./exp/already_watched.test', 'w') as fw:
    fw.write('%s\n' % ('\n'.join(test_features)))

#####
#####
#####

