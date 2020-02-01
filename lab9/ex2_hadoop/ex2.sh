#!/bin/bash


n=`cat input.txt | wc -l`

eval "sed '5c N = $n' reducer.py > reducer_changed.py"


reducer='reducer_changed.py'
mapper='mapper.py'

#cat input.txt | ./starter.py > privateinput.txt

hdfs dfs -rm -r temp*
hdfs dfs -mkdir tempinput

hdfs dfs -copyFromLocal input.txt tempinput

cmd='hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -files $reducer,$mapper -mapper $mapper -reducer $reducer '

input='tempinput'
output='000'
for((i=1;i<20;i++));
do
    echo "Processing_$i"
    output="tempoutput_$i"
    eval "$cmd -input $input -output $output"
    input=$output
    eval "hdfs dfs -rm -r $input/_SUCCESS"
    hdfs dfs -cat $input/* | sort
done
hdfs dfs -cat $input/* | sort  > result.txt
cat result.txt
rm $reducer
