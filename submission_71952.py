# CTRL CLICK -> Multicursor
# CTRL D -> Multicursor next occurence
# CTRL K -> Mutlicursor skip next occurence
# CTRL X -> Delete an entire line
# CTRL SHIFT SPACE -> Select a string
# CTRL SHIFT UP/DOWN -> Move a line
# CTRL BRACKET -> Indent dedent 
# CTRL L -> Select a line
# CTRL SHIFT M -> Select contents inside a bracket

from collections import defaultdict
from collections import deque

num_airports, num_tickets = map(int, raw_input().split())
graph_size = num_airports * 2 + 1

# Initialize Graph as a dictonary of arrays
# Airport i connects to graph[i] places
graph  = [set() for i in range (graph_size)]
# The cost of buying out Airport i to j is weight[i][j]
capacities = defaultdict(lambda: defaultdict(int))
flows = defaultdict(lambda: defaultdict(int))

# Add flights to the graph, make the weight equal to the total cost
for _ in range (num_tickets):
	leaving_from, going_to, num_tickets, cost = map(int, raw_input().split())
	graph[leaving_from].add(going_to + num_airports)
	capacities[leaving_from][going_to + num_airports] = num_tickets * cost
	
	# Initialize residual
	graph[going_to + num_airports].add(leaving_from)
	if not capacities[going_to + num_airports][leaving_from]:
		capacities[going_to + num_airports][leaving_from] = 0

# Deal with bribes
bribe = map(int, raw_input().split())
for port_index in range (1, num_airports + 1):
	graph[port_index + num_airports].add(port_index)
	capacities[port_index + num_airports][port_index] = bribe[port_index - 1]

	# Initialize residual
	graph[port_index].add(port_index + num_airports)
	if not capacities[port_index][port_index + num_airports]:
		capacities[port_index][port_index + num_airports] = 0

# Add in the the sink conditions
ending_airports = [2, 3, 4]
end_label = graph_size
for port in ending_airports:
	graph[port].add(end_label)

# Debug print graph and capacities
"""
for n in graph:
	print (n)
for x, y in capacities.items():
	print(x, y)
for x, y in flows.items():
	print(x, y)
	"""

# === We are done making our graph, now run Ford Fulkerson == 

# This is a function to reconstruct a path given the results of the BFS, and update the flows
prev = [0]*(graph_size)
def path_reconstruction(source, end_point):
	min_weight = float("inf")
	end = end_point

	while end_point != source:
		min_weight = min(min_weight, capacities[prev[end_point]][end_point] - flows[prev[end_point]][end_point]) 
		end_point = prev[end_point]
		
	# At this point we have the minweight of the path, now update flows
	while end != source:
		flows[prev[end]][end] += min_weight
		end = prev[end]

# This is a BFS that only visits vertices if they are not saturated, returns the sink if so, false otherwise
def bfs(g, source):
	# Initialize queue
	queue = deque()
	queue.append(source)
	visited = set()

	while queue:
		front = queue.popleft()
		if front not in visited:
			visited.add(front)
			# If it is a sink
			if front in ending_airports:
				return front
			# Otherwise, look at all children who haven't been visited
			for connection in graph[front]:
				if connection not in visited and capacities[front][connection] - flows[front][connection] > 0:
					queue.append(connection)
					prev[connection] = front
	return -1

# Ford Fulkerson
run = True
while run:
	finished = bfs(graph, 1 + num_airports)
	if finished >= 0:
		path_reconstruction(1 + num_airports, finished)
	else:
		run = False

print (flows[1+num_airports][1])






