# A node of a disjoint set
class dset: 
    def __init__(self, p, r): 
        # Each node has a parent and a rank
        self.r = r
        self.p = p 
         
def find(node): 
    if sets[node].p != node: 
        sets[node].p = find(sets[node].p)
    return sets[node].p 

  
# union set1 and set2
def union(n1, n2): 
    set1 = find(n1)
    set2 = find(n2)
    if (set1 != set2):
        if sets[set2].r > sets[set1].r: 
            sets[set1].p = set2 
        elif sets[set1].r > sets[set2].r: 
            sets[set2].p = set1
        else: 
            sets[set1].p = set2 
            sets[set2].r  += 1

total = 0
N, M, Q = map(int, raw_input().split())
sets = [0]
for u in range (1, 2*N+1):
    sets.append(dset(u, 0))

def query1 (n1, n2):
    union(n1+N, n2)
    union(n1, n2+N)

def query2 (n1, n2):
    global total
    if (find(n1+N) == find(n2) or find(n1) == find(n2 + N)):
        total += 1

for i in range(M):
    n1, n2 = map(int, raw_input().split())
    union(n1+N, n2)
    union(n1, n2+N)

for i in range(Q):
    q, n1, n2 = map(int, raw_input().split())
    if q == 1:
        query1(n1, n2)
    elif q == 2:
        query2(n1, n2)

print (total)



