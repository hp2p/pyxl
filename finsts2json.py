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


e_csv = open('2016_Finantial_statements.txt', 'rb').read().decode('euc-kr')
e_csv += open('2016_Income_statements.txt', 'rb').read().decode('cp949')


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


def print_item(item, cond1, line):
    if (item in line) and cond1:
	print "##########", item
	ws = line.split('\t')
	#for w in ws[-3:]:
	for w in ws:
	    print w
	print

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s start_year" % sys.argv[0]
	sys.exit(-1)

    lines = e_csv.splitlines()
    for line in lines:
        if u'동국제약' in line:

	    print_item(u'자산총계', True, line)
	    print_item(u'부채총계', u'자본과' not in line, line)
	    print_item(u'자본총계', True, line)
	    print_item(u'매출\t', True, line)
	    print_item(u'영업이익', True, line)
	    print_item(u'당기순이익', u'귀속' not in line, line)
	    print_item(u'연결순이익', True, line)
	    print_item(u'주당이익', True, line)

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
    
    
