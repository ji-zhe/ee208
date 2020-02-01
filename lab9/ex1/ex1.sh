#!/bin/bash
hdfs dfs -rm -r temp*
hdfs dfs -mkdir tempinput
hdfs dfs -copyFromLocal input/* tempinput
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
    -files mapper.py,reducer.py \
    -mapper mapper.py \
    -reducer reducer.py \
    -input tempinput \
    -output tempoutput;
hdfs dfs -copyToLocal tempoutput/p* result.txt
cat result.txt
