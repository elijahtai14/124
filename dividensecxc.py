N, T = map(int, raw_input().split())
vc = map(int, raw_input().split())
t = map(int, raw_input().split())
t.sort()

possiblePeaks = []

maxval = 0

for boothindex in range (0, len(vc)):
	if (vc[boothindex] > maxval):
		possiblePeaks.append(boothindex)
		maxval  = vc[boothindex]


vcsum = vc[:]
for i in range (1, N):
	vcsum[i] = vcsum[i] + vcsum[i-1]
vcsum.insert(0,0)

cutoff = 0

for i in range (0, T):
	if t[i] > possiblePeaks[len(possiblePeaks)-1]:
		cutoff = i


# Does not work if startInd >= n - 1
# Only works if startInd <= n - 2

TOTAL = 0;

def calc (tInd, startInd):
	global TOTAL
	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaks) and possiblePeaks[i] < min(t[tInd], N)):
		m = findmoney(tInd, possiblePeaks[i])
		#print ("findmoney( "+str(tInd)+","+str(i)+" )" + " = " + str(findmoney(tInd, i)))
		if m > money:
			money = m
			ind = i
		i = i + 1
	TOTAL += money
	#print (money)
	return ind


def calc2 (tInd, startInd):
	global TOTAL
	moneys = []
	moneysind = []

	money = 0
	ind = 0
	i = startInd
	while (i < len(possiblePeaks) and possiblePeaks[i] < min(t[tInd], N)):
		m = findmoney(tInd, possiblePeaks[i])
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
		possiblePeaks.pop(j)

	#print (money)
	return ind

# Returns the amount of money if goes to ind and stays.
def findmoney(tInd, ind):
	#print (str(vc[ind]) +" "+ str(t[tInd]-ind) +" " +str(vcsum[ind]))
	return vc[ind] * (t[tInd]-ind) + vcsum[ind]

index = 0


for i in range (0, cutoff):
	index = calc2(i, index)


for i in range (cutoff, T):
	index = calc(i, index)



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
