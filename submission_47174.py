from collections import defaultdict
import heapq

n, m, k = map(int, raw_input().split())

# where weight[u,v] is the weight from u to v
weights = {}

# the current graph were graph[v] gives a set of connecting vertices
black = defaultdict(set)
black_amount = 0

for i in range(1, n + 1):
	weights[i] = {}

# We create our weights and graph
for i in range(0, m):
    temp1, temp2, temp3 = map(int, raw_input().split())
    black_amount += temp3

    black[temp1].add(temp2)
    black[temp2].add(temp1)

    weights[temp1][temp2] = temp3
    weights[temp2][temp1] = temp3

# For white edges we take the minimal
for i in range(0, k):
    temp1, temp2, temp3 = map(int, raw_input().split())
    black[temp2].add(temp1)
    black[temp1].add(temp2)

    if temp1 in weights and temp2 in weights[temp1]:
    	weights[temp1][temp2] = min(weights[temp1][temp2], temp3)
    else:
    	weights[temp1][temp2] = temp3

    if temp2 in weights and temp1 in weights[temp2]:
    	weights[temp2][temp1] = min(weights[temp2][temp1], temp3)
    else:
    	weights[temp2][temp1] = temp3


def prim (graph, weights, s, N):
	weight = 0

	mstset = set()
	edges = []
	heapq.heappush(edges, (0, s))

	while len(edges) > 0:
		#print (edges)
		w, v = heapq.heappop(edges)
		if v not in mstset:
			weight += w
			mstset.add(v)
			#print ("adding " + str(v) + " " + str(w))
			for connectingvertex in graph[v]:
				if connectingvertex not in mstset:
					heapq.heappush(edges, (weights[v][connectingvertex], connectingvertex))
	return weight

print(black_amount - prim(black, weights, 1, n))
