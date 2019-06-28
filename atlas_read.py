#!/usr/bin/env python

import sys, os
import subprocess
from math import sqrt
import numpy as np

paramMessage = ' expected. Usage: python %s FileName' % __file__

def mean(lst):
    """calculates mean"""
    return sum(lst) / len(lst)

def stddev(lst):
    """returns the standard deviation of lst"""
    mn = mean(lst)
    variance = sum([(e-mn)**2 for e in lst]) / len(lst)
    return sqrt(variance)

def main(argv):
    try:
        FileName = sys.argv[1]
        if not os.path.exists(FileName):
            print 'FedName' + paramMessage
            sys.exit(2)
    except:
        print 'FileName' + paramMessage
        sys.exit(2)
    
    categories = 'Categories'
    atlas_read = 'Read'
    atlas_mean = 0
    atlas_read_dev = 'Read Error'
    resdata = []
    rdata = []

    rawdata = subprocess.Popen("awk -F \"[^[:alnum:]:.-]+\" 'BEGIN{}/real/{N=$2;print\"{\\\"real\\\":\\\"\"N\"\\\"},\"}END{}' < %s" % (FileName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    arrdata = rawdata.split('\n')
    for l in arrdata:
        try:
            resdata.append(eval(l))
        except:
            pass
    
    for i in resdata:
        print i
        rdata.append(float(i[0]['real']))
                            
        atlas_read += (',%s') % (i[0]['real'])
        atlas_mean += float(i[0]['real'])
#        atlas_read_dev += (',[%s,%s]') % (i['read'] - i['readdev'], i['read'] + i['readdev'])
    
    stdev = stddev(rdata)     
    print categories
    print atlas_read
    print mean(rdata)
    print stddev(rdata)
    print(np.std(np.array(rdata)))

    for i in resdata:
        atlas_read_dev += (',[%s,%s]') % (float(i[0]['real']) - stdev, float(i[0]['real']) + stdev)
    
    atlas_read_dev += (',[%s,%s]') % (mean(rdata) - stdev, mean(rdata) + stdev)
    print atlas_read_dev
    
if __name__ == "__main__":
    main(sys.argv[1:])