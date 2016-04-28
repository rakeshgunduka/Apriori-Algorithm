from __future__ import division
from nltk import regexp_tokenize
import csv,copy

###########Globals###########
d = []
d_main = {}
dv = []
count = {}
allowed = {}
last_level = 0

###########Join two sets###########
def join(d1,d2):
	if type(d1) == list and type(d2) == list:
		rls = []	
		for j in d2:
			tmpls = copy.copy(d1)
			if j not in d1:
				tmpls.append(j)
				rls.append(tmpls)		
		return rls
	else:
		return [d1,d2]

###########Get Pairs of Dataset###########
def getpairss(ls,level):
	d1 = d2 = ls
	substr = []
	td = []
	for i in d1:
		for j in d2:
			if j>i:
				val = join(i,j)
				if level != 1:
					for k in val:
						if k == sorted(k):
							if k not in td:
								td.append(k)
				else:
					td.append(val)		
	return td

###########Check For Support###########
def check_for_support(d_val,level,support):
	ls = []
	for j,i in enumerate(count[level]):
		if i >= support:
			ls.append(d_val[j])
	return sorted(ls)

###########Check Value in Dataset###########
def checkinlist(check_val,in_data):
	if type(check_val) == list:
		for i in check_val:
			if i in in_data:
				continue
			else:
				return False
		return True
	else:
		if check_val in in_data:
			return True
		else:
			return False

###########Count Occurences of Dataset###########
def count_occurencee(d_val,d):
	d_valcnt = [0 for i in range(len(d_val))]
	for i in d_val:
		for j in d:
			if checkinlist(i,j):
				d_valcnt[d_val.index(i)] += 1
	return d_valcnt

###########Apriori Function###########
def apriori(level,d_val,support):
	global last_level
	last_level = level-1
	if level != 1:
		d_val = getpairss(allowed[level-1],level-1)
		
	print "\n",30*"*","level",level,"*"*30
	print "dataset(d_val) :",d_val
	print "Support(support) :",support
	print "Pairs :",d_val
	count[level] = count_occurencee(d_val,d)
	ret_val = check_for_support(d_val,level,support)
	if len(ret_val) != 0:
		allowed[level] = ret_val
	else:
		print "There is no support further, Stopping Here"
		return
	ls = [i for i in count[level] if i >= support]
	count[level] = ls
	print "Count for level",level,":",count[level]
	print "Allowed :",allowed[level]
	level += 1
	apriori(level,d_val,support)

###########Check For Stronges Associtaion###########
def	check_strongassoc(freq,val):
	ls = []
	threshold = 70
	for i in val:
		cal_val = ((count[len(freq)][allowed[len(freq)].index(freq)]/count[len(i)][allowed[len(i)].index(i)])*100)
		if cal_val > threshold:
			ls.append(i)
	return ls

###########Check for Association Rule for frequent sets###########
def assoc_rules(freqsets):
	cs = {}
	for j,i in enumerate(freqsets):
		val = getpairss(i,level)
		#print val
		for k in i:
			val.append(k)
		cs[j] = check_strongassoc(i,val)
	ls = ([len(cs[i]) for i in cs])
	return freqsets[ls.index(max(ls))]

###########Main###########	
if __name__ == '__main__':
	print "\n",23*"*","Apriori Algorithm","*"*21
	ch = int(input("Mode of input\n1: Manual Dataset\n2: Csv File \nChoice : "))
	d_valcnt = {}
	if ch == 1:
		n = int(input("Length of Dataset : "))
		print "Enter Data followed by space(Eg. 1 5 3)\nID","\t","Itemsets"
		for i in range(n):
			print i+1,
			d.append([x for x in raw_input("\t").split()])
	else:
		file_name = raw_input("Enter Filename(.csv) :")
		reader = csv.reader(open(file_name))
		for row in reader:
			d.append(row)
		del d[0]	
	print "\n",23*"*","Itemsets Provided","*"*21
	for index,lists in enumerate(d):
		if ch == 2:
			for strs in lists:
				tokens = regexp_tokenize(strs,r',',gaps=True)
			d[index] = tokens
		for j in d[index]:
			if j not in dv:
				dv.append(j)
				d_valcnt[j] = 0
		print d[index]
	
	support = 2
	level = 1
	dv = sorted(dv)
	apriori(level,dv,support)
	print "\n",20*"*","Applying Association Rules","*"*21
	freq_itsemsets = [j for i in allowed for j in allowed[i]]
	print "Freq_itsemsets :",freq_itsemsets
	most_freqset = assoc_rules(allowed[last_level])
	print "\n",23*"*","Final Frequent Patterns","*"*21
	for i in allowed:
		for j in allowed[i]:
			print j," "*10,":",count[len(j)][allowed[len(j)].index(j)]

	print "\n",23*"*","Most Frequent Pattern","*"*21
	print most_freqset
