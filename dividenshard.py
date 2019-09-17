N, T = map(int, raw_input().split())
vc = map(int, raw_input().split())
t = map(int, raw_input().split())
t.sort()

# Make a list of even and odd times
tEven = []
tOdd = []
for z in t:
	if z % 2 == 0:
		tEven.append(z)
	else:
		tOdd.append(z)
"""
print (tEven)
print (tOdd)
"""

# Make a list of even and odd possible indices
possiblePeaksEven = []
possiblePeaksOdd = []

# Maxval and Possible Peaks
maxval = 0
for boothindex in range (0, len(vc)-1):
	if (vc[boothindex] + vc[boothindex + 1] > maxval):
		possiblePeaksEven.append(boothindex)
		possiblePeaksOdd.append(boothindex)
		maxval  = vc[boothindex] + vc[boothindex + 1]
""""
print (possiblePeaksEven)
print (possiblePeaksOdd)
"""

# Walking Sums
vcsum = vc[:]
for i in range (1, N):
	vcsum[i] = vcsum[i] + vcsum[i-1]
vcsum.insert(0,0)


# CutOffs
cutoffEven = 0
for i in range (0, len(tEven)):
	if tEven[i] > possiblePeaksEven[len(possiblePeaksEven)-1]:
		cutoffEven = i

# CutOffs
cutoffOdd = 0
for i in range (0, len(tOdd)):
	if tOdd[i] > possiblePeaksOdd[len(possiblePeaksOdd)-1]:
		cutoffOdd = i


# Does not work if startInd >= n - 1
# Only works if startInd <= n - 2

TOTAL = 0;

def calcEven (tInd, startInd):
	global TOTAL
	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaksEven) and possiblePeaksEven[i] < min(tEven[tInd], N)):
		m = findmoneyEven(tInd, possiblePeaksEven[i])
		#print ("findmoneyEven( "+str(tInd)+","+str(i)+" )" + " = " + str(findmoneyEven(tInd, i)))
		if m > money:
			money = m
			ind = i
		i = i + 1
	TOTAL += money
	#print (money)
	return ind

def calcOdd (tInd, startInd):
	global TOTAL
	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaksOdd) and possiblePeaksOdd[i] < min(tOdd[tInd], N)):
		m = findmoneyOdd(tInd, possiblePeaksOdd[i])
		#print ("findmoneyOdd( "+str(tInd)+","+str(i)+" )" + " = " + str(findmoneyOdd(tInd, i)))
		if m > money:
			money = m
			ind = i
		i = i + 1
	TOTAL += money
	#print (money)
	return ind


def calc2Even (tInd, startInd):
	global TOTAL
	moneys = []
	moneysind = []

	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaksEven) and possiblePeaksEven[i] < min(tEven[tInd], N)):
		m = findmoneyEven(tInd, possiblePeaksEven[i])
		moneys.append(m)
		moneysind.append(i)
		#print ("findmoney( "+str(tInd)+","+str(i)+" )" + " = " + str(findmoney(tInd, i)))
		if m > money:
			money = m
			ind = i
		i = i + 1		
	TOTAL += money

	removethese = []

	maxmoneys = moneys[len(moneys)-1]
	l = len(moneys) 

	for j in range(l - 1, ind, -1):
		if moneys[j] < maxmoneys:
			removethese.append(moneysind[j])
		else:
			maxmoneys = moneys[j]

	for j in removethese:
		possiblePeaksEven.pop(j)

	#print (money)
	return ind

def calc2Odd (tInd, startInd):
	global TOTAL
	moneys = []
	moneysind = []

	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaksOdd) and possiblePeaksOdd[i] < min(tOdd[tInd], N)):
		m = findmoneyOdd(tInd, possiblePeaksOdd[i])
		moneys.append(m)
		moneysind.append(i)
		#print ("findmoney( "+str(tInd)+","+str(i)+" )" + " = " + str(findmoney(tInd, i)))
		if m > money:
			money = m
			ind = i
		i = i + 1		
	TOTAL += money

	removethese = []

	maxmoneys = moneys[len(moneys)-1]
	l = len(moneys) 

	for j in range(l - 1, ind, -1):
		if moneys[j] < maxmoneys:
			removethese.append(moneysind[j])
		else:
			maxmoneys = moneys[j]

	for j in removethese:
		possiblePeaksOdd.pop(j)

	#print (money)
	return ind



# Returns the amount of money if goes to ind and oscilates.
def findmoneyEven(tInd, ind):
	result = 0
	time = tEven[tInd] - ind
	if time % 2 != 0:
		result += vc[ind]
	result += (vc[ind] + vc[ind + 1]) * (time / 2) + vcsum[ind]
	return result

def findmoneyOdd(tInd, ind):
	result = 0
	time = tOdd[tInd] - ind
	if time % 2 != 0:
		result += vc[ind]
	result += (vc[ind] + vc[ind + 1]) * (time / 2) + vcsum[ind]
	return result

index = 0


for i in range (0, cutoffOdd):
	index = calc2Odd(i, index)


for i in range (cutoffOdd, len(tOdd)):
	index = calcOdd(i, index)

index = 0

for i in range (0, cutoffEven):
	index = calc2Even(i, index)


for i in range (cutoffEven, len(tEven)):
	index = calcEven(i, index)

print(TOTAL)


"""
# DEBUG 
def bf (tInd):
	vals = []
	for i in range (0, min(t[tInd], N)):
		vals.append(findmoney(tInd, i))
	return max(vals)

TOT = 0
for tInd in range (0, T):
	TOT += bf(tInd)

print (TOT)
"""
