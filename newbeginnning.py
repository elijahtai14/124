

from collections import defaultdict

n, m, k = map(int, raw_input().split())

graph = defaultdict(set)

for i in range (0, m):
	temp1, temp2 = map(int, raw_input().split())
	graph[temp1].add(temp2)
	graph[temp2].add(temp1)

vacant = [int(s) for s in raw_input().split()]
vacant.sort()

"""
vacant = [1, 3, 6, 7]
vacant.sort()
graph = {
	1: set([2]),
	2: set([1, 3]),
	3: set([2, 4]),
	4: set([3, 5]),
	5: set([4, 6]),
	6: set([5, 7]),
	7: set([6])
}

"""

# g is the graph, s is a list of sources.
def BFS (g, s):
	chang = False

	q = [[] for i in range (0, len(s))]
	visited = [-1 for i in range (0, len(g))]

	if 2 in g[1] and (2 in s) and (1 in s):
		return [1, 2]

	for i in range (0, len(s)):
		# Insert s[i], the source, to its own queue
		q[i].insert(0, s[i])
		# Toggle that the source has visited itself
		visited[s[i]-1] = s[i]

		for v in g[s[i]]:
			if v in s:
				return [s[i], v]


	# While the minimal distance has not been found
	while True:
		# For each source index
		cyclemin = [float("inf"), 0]
		changed = False
		for source in range(0, len(s)):
			if len(q[source]) != 0:
				# CYCLE!
				cyclenum = len(q[source])
				# THIS IS ONE CYCLE!
				for i in range(0, cyclenum):
					v = q[source].pop()
					for ver in g[v]:
						if visited[ver-1] == -1:
							visited[ver-1] = s[source]
							q[source].insert(0,ver)
						elif visited[ver-1] != s[source]:
							cyclemin = min(cyclemin, sorted([s[source], visited[ver-1]]))
							changed = True
		if (changed):
			return cyclemin

answ = BFS(graph, vacant)
print (str(answ[0])+" "+str(answ[1]))
