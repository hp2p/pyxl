#! /usr/bin/python

import sys
import json

def good_company(company):

    def increasing(data, tolerance):

	if not data:    return False

        di = len(data)-1
        while di > 0:
            if data[di] < data[di-1]:
	        tolerance -= 1
	        if tolerance < 0:
	            return False
	    di -= 1    
	return True

    #if increasing(company['EPS'], 2) and \
    #   increasing(company['NET_INCOME'], 2) and \
    #if   increasing(company['SALES'], 0):
    if increasing(company['NET_INCOME'], 1):
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage : %s file_name" % sys.argv[0]
        sys.exit(-1)

    reload(sys)
    sys.setdefaultencoding('utf-8')

    fp = open(sys.argv[1])

    companies = json.load(fp)

    num_good_company = 0
    for cc in companies:
	if cc['SALES'] and cc['SALES'][0] > 0 and good_company(cc):
	    num_good_company += 1
            print cc['name']
	    print 'EPS =        ', cc['EPS']
	    print 'NET_INCOME = ', cc['NET_INCOME']
	    print 'SALES =      ', cc['SALES']
	    print 'INC/SALES =  ', [(cc['SALES'] and cc['SALES'][i]) and 100*cc['NET_INCOME'][i]/cc['SALES'][i] or 0 for i in range(len(cc['EPS']))]
	    print 'ROE =        ', [100*cc['NET_INCOME'][i]/cc['EQUITY'][i] for i in range(len(cc['EPS']))]
	    print 'DEBT  =      ', cc['DEBT']
	    print 'EQUITY  =    ', cc['EQUITY']
	    print 'DEBT/EQUITY =', [100*cc['DEBT'][i]/cc['EQUITY'][i] for i in range(len(cc['EPS']))]
	    print

    print 'num_good_company = ', num_good_company
