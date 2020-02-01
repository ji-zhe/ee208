#!/bin/bash

n=`cat input.txt | wc -l`

cat input.txt | ./starter.py > privateinput.txt


inputfile='privateinput.txt'
for((i=1;i<1000;i++));
do
#    echo "process_$i"
    cat $inputfile | ./mapper.py | sort | ./reducer.py $n | sort > middle_$i
    outputfile="middle_$i"
#    cat $inputfile | ./format.py | sort
    flag=`diff $inputfile $outputfile`
    if [ -z "$flag" ]
    then
        echo "total iterations:" $i
        break;
    fi
    inputfile=$outputfile
done

cat $inputfile | ./format.py | sort  > final.txt

rm middle_*
rm privateinput.txt

echo "final result:"
cat final.txt
