#!/usr/bin/env python
import sys
id1 = id2 = None
children = value = None
count = 0


for line in sys.stdin:
    data = line.strip().split()
    if len(data)>1 and  data[1]!= '@':
        count += 1
        if count >= 2:
            print '%s\t%s' % (id1,0.0) #output the previous one with value 0 to avoid being lost
        id1 = data[0]
        value = float(data[1]) 
    else:#This the link relation
        print '%s\t%s' % (data[0], ' '.join(data[1:]))
        id2 = data[0]
        children = data[2:]
    if id1 == id2 and id1:
        v = value / len(children)
        for child in children:
            print '%s\t%s' % (child,v)
        print '%s\t%s' % (id1,0.0)
        id1 = id2 = None
        count = 0
