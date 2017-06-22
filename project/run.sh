mkdir exp
python3.5 code/generate_pairs.py ./assets/events_train.csv ./assets/events_test.csv
python3.5 code/generate_features.py ./assets/events_train.csv assets/events_test.csv ./exp/train.pairs ./exp/test.pairs
paste -d ' ' ./exp/time_diff.test ./exp/pop.test ./exp/last_watched.test > ./exp/test.combined
python3.5 code/combine.py ./exp/test.combined ./submit/manual.csv > predict.csv
