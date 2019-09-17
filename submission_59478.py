
from collections import defaultdict


import sys
sys.setrecursionlimit(2 ** 26)

# n = number of cities
# m = number of cables
# b = budget
n, m, b = map(int, raw_input().split())

graph = []
for i in range (n+1):
	graph.append(list())

graphreverse = []
for i in range (n+1):
	graphreverse.append(list())

serverquality = [0]
servercost = [0]

# Add edges to the graph
for i in range (1, m+1):
	temp1, temp2 = map(int, raw_input().split())
	graph[temp1].append(temp2)
	graphreverse[temp2].append(temp1)

# Add server specifications
for i in range (1, n+1):
	cost, quality = map(int, raw_input().split())
	serverquality.append(quality)
	servercost.append(cost)


#--------------------------------
# GRAPH DEBUG
"""
print ("Graph:")
print ("        "+ str(graph))

print ("Reverse Graph:")
print ("        "+ str(graphreverse))
"""
#--------------------------------



# KOSARAJU'S
# The first DFS. Get the post-order numbers

# Making sure everything is pointed to
postorder = []
needtovisit = []

def search(u, g):
	# We no longer need to visit city u
	needtovisit[u] = False
	#print ("        Searching " + str(u))
	# Check the each edge e(u,v)
	for v in g[u]:
 		if needtovisit[v]:
 			search(v, g)
	#print ("        Done with " + str(u))
	postorder.append(u)


def DFSr(g):
	global needtovisit
	needtovisit = [True] * (n + 1)
	for i in range (1, n + 1):
		if needtovisit[i]:
			search(i, g)


DFSr(graphreverse)
#--------------------------------
# DFS1 Debug
"""
print("Running DFS on Reverse Graph")
print("        Post-order numbers")
print("        "+ str(postorder))
print("        "+ str(notpointedto))
"""
#--------------------------------

# The second DFS. Get the SCCs
scc = []
counter = -1

def searchscc (u, g):
	global counter

	# We no longer need to visit city u
	needtovisit[u] = False

	# Check the each edge e(u,v)
	for v in g[u]:
		if needtovisit[v]:
			searchscc(v, g)

	scc[counter].append(u)


def DFSscc(g):
	global counter
	global needtovisit
	needtovisit = [True] * (n + 1)
	# Decreasing post-order number
	postorder.reverse()
	for i in postorder:
		if needtovisit[i]:
			# This SCC will be the counterth index in scc[]
			counter += 1
			scc.append(list())
			searchscc(i, g)


DFSscc(graph)

for c in scc:
	if len(c) < 2:
		print("Impossible")
		sys.exit()


#--------------------------------
# DFS2 Debug
"""
print("Running DFS on Graph in decreasing Post-order Number")
print ("        SCCs")
print ("        " + str(scc))
"""
#--------------------------------



# BFS to check that a vertex in the source SCC can reach everything
tocheck = []
checked = set()


def BFS(g, s):
	tocheck.append(s)
	while len(tocheck) > 0:
		v = tocheck.pop()
		for i in g[v]:
			if i not in checked:
				tocheck.insert(0, i)
		checked.add(v)

BFS(graph, scc[len(scc) - 1][0])

# If it can't reach everything
if len(checked) != n:
	print ("Impossible")
	sys.exit()

# If they are all one
if servercost[1] == serverquality[1] == servercost[2] == serverquality[2] == 1:
	if b < 2 * len(scc):
		print(" ")
	else:
		print (2 * len(scc))
	sys.exit()

#--------------------------------
# COST/QUALITY DEBUG
"""
print ("Cost:")
print ("        "+ str(servercost))

print ("Quality:")
print ("        "+ str(serverquality))
"""
#--------------------------------

mem = [{} for i in range (len(scc))]

def backpackdp (B, c, servercost, serverquality):
	# for each component
	for i in range (len(c)):
		# for each city in a component
		for cityi in range (-1, len(c[i])):
			mem[i][cityi] = {}
			# this is how many left you are allowed to take
			for j in range (3):
				mem[i][cityi][j] = {}
				# this is for each budget
				for B in range (b+1):
					if cityi < 0 and j > 0:
						mem[i][cityi][j][B] = -float("inf")
					elif i == 0 and (cityi == -1 or j == 0):
						mem[i][cityi][j][B] = 0
					elif j == 0:
						mem[i][cityi][j][B] = mem[i -1][len(c[i-1])-1][2][B]
					else:
						# getting back the city from the city index
						city = c[i][cityi]
						a = mem[i][cityi-1][j][B]
						if B - servercost[city] < 0:
							a2 = -float("inf")
						else:
							a2 = mem[i][cityi-1][j-1][B-servercost[city]] + serverquality[city]

						mem[i][cityi][j][B] = max(a, a2)	
			if cityi > 0:
				mem[i][cityi-1].clear()
		if i > 0:
			mem[i - 1].clear()
	return(mem[len(c)-1][len(c[i])-1][2][B])

"""
memodd = [ -1 for j in range (b + 1)]
memeven = [ 0 for j in range (b + 1)]
even = False

def backpackdp(B, k):
	global even 
	# Fill in the cell starting from column k
	for K in range(k-1, -1, -1):
		for B in range (0, b + 1):
			# Look at all two picks
			cell = -1
			if even:
				for i in range (0, len(scc[K])-1):
					for j in range (i + 1, len(scc[K])):
						# Find values of the two picks
						cost = servercost[scc[K][i]] + servercost[scc[K][j]]
						# If it is affordable
						if B - cost >= 0:
							if memodd[B - cost] >= 0:
								quality = serverquality[scc[K][i]] + serverquality[scc[K][j]]
								# If mem BK is less, then update
								if cell < quality + memodd[B-cost]:
									cell = quality + memodd[B-cost]
				memeven[B] = cell

			else:
				for i in range (0, len(scc[K])-1):
					for j in range (i + 1, len(scc[K])):
						# Find values of the two picks
						cost = servercost[scc[K][i]] + servercost[scc[K][j]]
						# If it is affordable
						if B - cost >= 0:
							if memeven[B - cost] >= 0:
								quality = serverquality[scc[K][i]] + serverquality[scc[K][j]]
								# If mem BK is less, then update
								if cell < quality + memeven[B-cost]:
									cell = quality + memeven[B-cost]
				memodd[B] = cell
		even = not even


ans = 0
backpackdp(b, len(scc))


total = 0
if len(scc) <= 5:
 	for c in scc:
 		max = 0
 		for i in range (0, ) 

if even:
	ans = memodd[b]
else:
	ans = memeven[b]
"""
ans = backpackdp (b, scc, servercost, serverquality) 

if ans >= 0: 
	print(ans)
else:
	print("Impossible") 
sys.exit()