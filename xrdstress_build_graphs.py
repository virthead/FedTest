#!/usr/bin/env python

import sys, os
import subprocess
import datetime

paramMessage = ' expected. Usage: python %s FedName{msk|spb} Size{1|10|100|} ReportDate{yyyy-mm-dd}' % __file__

def main(argv):
    StorName = ['eos', 'dcache']
    try:
        FedName = sys.argv[1]
        if FedName != 'msk' and FedName != 'spb':
            print 'FedName' + paramMessage
            sys.exit(2)
    except:
        print 'FedName' + paramMessage
        sys.exit(2)
    
    try:
        Size = int(sys.argv[2])
    except:
        print 'Size' + paramMessage
        sys.exit(2)
    
    try:
        ReportDate = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%d').date()
    except:
        print 'ReportDate' + paramMessage
        sys.exit(2)
        
    categories = 'Categories'
    eos_read = 'EOS Read'
    eos_read_dev = 'EOS Read Error'
    eos_write = 'EOS Write'
    eos_write_dev = 'EOS Write Error'
    dcache_read = 'dCache Read'
    dcache_read_dev = 'dCache Read Error'
    dcache_write = 'dCache Write'
    dcache_write_dev = 'dCache Write Error'
    for stor in StorName:
        resdata = []
        rawdata = subprocess.Popen("awk -F \"[^[:alnum:]:.-]+\" 'BEGIN{}/Host:/{H=$2;D=$4}/all thread read/{R=$7;RD=$11}/all thread write/{W=$7;WD=$11;print\"{\\\"host\\\":\\\"\"H\"\\\",\\\"date\\\":\\\"\"D\"\\\",\\\"read\\\":\"R\",\\\"readdev\\\":\"RD\",\\\"write\\\":\"W\",\\\"writedev\\\":\"WD\"}\"}END{}' < results/xrdstress_%s_%s_%s_%s.log" % (stor, FedName, Size, ReportDate), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        arrdata = rawdata.split('\n')
        for l in arrdata:
            try:
                resdata.append(eval(l))
            except:
                pass
        for i in resdata:
#             print stor
#             print i
#             print i['host']
#             print i['writedev']

#                categories += (',\'%s\'') % (i['host'][0:len(i['host']) - 1])
            if i['host'].find('kiae') != -1:
                categories += (',\'NRC KI\'')
            elif i['host'].find('pnpi') != -1:
                categories += (',\'PNPI\'')
            elif i['host'].find('jinr') != -1:
                categories += (',\'JINR\'')
            elif i['host'].find('msu') != -1:
                categories += (',\'SINP\'')
            elif i['host'].find('itep') != -1:
                categories += (',\'ITEP\'')
            elif i['host'].find('spbu') != -1:
                categories += (',\'SPbSU\'')
            
            if stor == 'eos':
                eos_read += (',%s') % (i['read'])
                eos_read_dev += (',[%s,%s]') % (i['read'] - i['readdev'], i['read'] + i['readdev'])
                eos_write += (',%s') % (i['write'])
                eos_write_dev += (',[%s,%s]') % (i['write'] - i['writedev'], i['write'] + i['writedev'])
            
            if stor == 'dcache':
                dcache_read += (',%s') % (i['read'])
                dcache_read_dev += (',[%s,%s]') % (i['read'] - i['readdev'], i['read'] + i['readdev'])
                dcache_write += (',%s') % (i['write'])
                dcache_write_dev += (',[%s,%s]') % (i['write'] - i['writedev'], i['write'] + i['writedev'])
            
    print categories
    print eos_read
    print eos_read_dev
    print eos_write
    print eos_write_dev
    
    print dcache_read
    print dcache_read_dev
    print dcache_write
    print dcache_write_dev
    
if __name__ == "__main__":
    main(sys.argv[1:])
