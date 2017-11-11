#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import json


reload(sys)
sys.setdefaultencoding('utf-8')


def remove_comma_in_digits(ss):
   ret = ''
   i = 0
   while i < len(ss):
       if ss[i] == '"':
	   i += 1
	   while ss[i] != '"':
	       if ss[i] != ',':
	           ret += ss[i]
	       i += 1
       else:
           ret += ss[i]
       i += 1
   return ret


e_csv = open('Earnings.csv', 'rb').read().decode('utf-8')


class Company:
    def __init__(self, code, name, start_year):
        self.code_ = code
	self.name_ = name
	self.start_year_ = start_year
	self.asset_ = []   
	self.debt_ = []
	self.equity_ = []
	self.sales_ = []
	self.opr_income_ = []
	self.net_income_ = []
	self.eps_ = []
	self.gross_profit_ = []
	self.cost_sales_ = []
	self.sell_admin_expense_ = []

    def __str2__(self):
        res = self.code_ + ' ' + self.name_ + (' [%d~]' % self.start_year_)

	data = (
	    ('ASSET',      self.asset_),
	    ('DEBT',       self.debt_),
	    ('EQUITY',     self.equity_),
	    ('SALES',      self.sales_),
	    ('OPR_INCOME', self.opr_income_),
	    ('NET_INCOME', self.net_income_),
	    ('EPS',        self.eps_)
	)

        for d in data:
	    res += '\n[%11s] ' % d[0]
	    for v in d[1]: 
	        res += '%7d ' % v

	return res

    def __str__(self):

	data = (
	    ('ASSET',      self.asset_),
	    ('DEBT',       self.debt_),
	    ('EQUITY',     self.equity_),
	    ('SALES',      self.sales_),
	    ('OPR_INCOME', self.opr_income_),
	    ('NET_INCOME', self.net_income_),
	    ('EPS',        self.eps_)
	)

        res = { 'code': self.code_,
	        'name': self.name_,
		'period': '[%d~]' % self.start_year_ } 

        for d in data:
	    res[d[0]] = d[1]

        res = json.dumps(res, ensure_ascii=False )

	return res


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s start_year" % sys.argv[0]
	sys.exit(-1)

    ORIG_START_I = 1996
    start_year = int(sys.argv[1])
    start_i = start_year - ORIG_START_I + 1
    
    line_no = 0
    companies = []
    
    for line in e_csv.splitlines():
        epss = 0
        if (u'유가증권' in line) or (u'코스닥' in line) or (u'코넥스' in line):
            code = line.split(',')[4]
            name = line.split(',')[8]
    	    company = Company(code, name, start_year)
    	    companies.append( company )
        else:
    
    	    '''
    	    for w in line.split(',')[1:]:
    	        if w and not w.lstrip('-+').isdigit():
    		    print name
    	            print w
    		'''

    	    def get_numbers(line):
    	        return [w and int(w) or 0 for w in line.split(',')[1:] ]
    
    	    line = remove_comma_in_digits(line)
            if (u'자산총계' in line):
                company.asset_ = get_numbers(line)[start_i:] 
            elif u'부채총계' in line:
                company.debt_ = get_numbers(line)[start_i:] 
    	    elif u'자본총계' in line:
    	        company.equity_ = get_numbers(line)[start_i:] 
    	    elif u'매출액' in line:
    	        company.sales_ = get_numbers(line)[start_i:] 
    	    elif u'영업이익' in line:
    	        company.opr_income_ = get_numbers(line)[start_i:] 
    	    elif (u'연결순이익' not in line) and (u'순이익' in line):
    	        company.net_income_ = get_numbers(line)[start_i:] 
    	    elif u'EPS' in line:
    	        company.eps_ = get_numbers(line)[start_i:] 
    
        line_no += 1
    
    
    sss = '[\n'
    for comp in companies:
        sss += str(comp) + ',\n\n'
    
    print sss[:-3], '\n\n]'
    
    
    { u'assets' : u'자산',
      u'liabilities' : u'부채',
      u'equity' : '자본',
      u'operating_income' : u'영업이익',
      u'net_income' : u'순이익',
      u'consolidated_income' : u'연결순이익',
      u'eps' : u'EPS',
      u'sales' : u'매출액',
      u'cost_of_sales' : u'매출원가',
      u'gross_profit' : u'매출총이익',
      u'selling_admin_expense' : u'판매비와 관리비'
    }
    
    
