#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import json


reload(sys)
sys.setdefaultencoding('utf-8')


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


if __name__ == "__main__":

    f = open('Earnings.csv', 'rb')
    e_csv = f.read().decode('utf-8')
    f.close()

    if len(sys.argv) < 2:
        print "Usage: %s start_year" % sys.argv[0]
	sys.exit(-1)

    ORIG_START_I = 1996
    start_year = int(sys.argv[1])
    start_i = start_year - ORIG_START_I + 1
    
    line_no = 0
    companies = {}
    
    for line in e_csv.splitlines():
        epss = 0
        if (u'유가증권' in line) or (u'코스닥' in line) or (u'코넥스' in line):
            code = line.split(',')[4]
            name = line.split(',')[8]
    	    company = Company(code, name, start_year)
    	    companies[code] = company
        else:
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
    
    f = open('2016_Finantial_statements_mod.txt', 'rb')
    lines = f.read().decode('euc-kr').splitlines()
    f.close()

    f = open('2016_Income_statements_mod.txt', 'rb')
    lines += f.read().decode('cp949').splitlines()
    f.close()

    invalid_codes = {}

    def get_number3(line):
	ret = []
	if 'USD' in line:
	    rate = 1085
	elif 'JPY' in line:
	    rate = 10
	elif 'CNY' in line:
	    rate = 170
	elif 'KRW' in line:
	    rate = 1
	else:
	    print 'ERROR. no USD JPY CNY KRW'
	    print
	    print
	    print

	for w in reversed(line.split('\t')):
	    w = w.replace(',', '')
	    if w:
	        if w.replace('-','').isdigit():
		    ret.append( ( (rate * int(w)) + 50000000)/100000000 )
		else:
		    break
        return ret
	        

    for line in lines:
        ws = line.split('\t')
	code = u'A' + ws[1][1:-1].encode('utf-8')
	name = ws[2].encode('utf-8')

	if code not in companies:
    	    company = Company(code, name, start_year)
    	    companies[code] = company
	else:
	    comp = companies[code]
	    if comp.name_ != name:
	        # print 'code = %s name = %s comp.name_ = %s' % (code, name, comp.name_)
	        comp.name_ = name

	if (u'자산총계' in line) or \
	   (u'부채총계' in line) or \
	   (u'자본총계' in line) or \
	   (u'\t당기순이익\t' in line) or \
	   (u'\t매출액\t' in line) or \
	   (u'\t영업이익\t' in line) or \
	   (u'\t주당이익\t' in line):

	        ns = get_number3(line)
		if len(ns) == 3:
		    ns = ns[1:]

	        if (u'자산총계' in line):
		    comp.asset_ += ns
		elif (u'부채총계' in line):
		    comp.debt_ += ns
		elif (u'자본총계' in line):
		    comp.equity_ += ns
		elif (u'당기순이익' in line):
		    comp.net_income_ += ns
	        elif (u'매출액' in line):
		    comp.sales_ += ns
		elif (u'영업이익' in line):
		    comp.opr_income_ += ns
		elif (u'주당이익' in line):
		    comp.eps_ += ns

    #for c in invalid_codes:
    #    print invalid_codes[c]


    sss = '[\n'
    for comp in companies.values():
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
    
    
