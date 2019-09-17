# The answer
answer = 0

# Constants for hashing formula
b = 29
p = 100000000003

# polyHASH MULTI hash rolling hash


#INPUTS
log_length, bug_length = map(int, raw_input().split())
# The string
compressed_log = raw_input()
# The bugs hashes
bug_hashes = {}
# The length of the bugs
bugs_len = set()

# LOOKUP TABLE
# The keyth entry stores b^(2^key)
pow_store = {0:b}

# === Helper Functions ===

def store_pow(dig):
	finished = pow_store.get(dig - 1)
	if not finished:
		store_pow(dig - 1) 
		finished = pow_store[dig - 1]

	finished = (finished ** 2) % p
	pow_store[dig] = finished

# Will compute a power of b^exp
def powb(exp):
	result = 1
	current_digit = 0
	bin_str = bin(exp)[::-1][:-2]
	for mask in bin_str:
		maskdigit = int(mask)
		if maskdigit:
			if not pow_store.get(current_digit):
				store_pow(current_digit)
			result = (result * pow_store[current_digit])%p
		current_digit += 1
	#print ("29^"+str(exp)+" = "+str(result))
	return result

# Returns hash value for a character char and a power p
def hash_letter(char, p):
	return (ord(char) - 64)*powb(p)

# Returns hash value for a character char and a power mult = b^k
def hash_letter_m(char, mult):
	return (ord(char) - 64)*mult

# Returns hash value for a string s
def forcehash(s):
	result = 0
	l = len(s) - 1
	for char in s:
		result += hash_letter(char, l)
		l -= 1
	#print ("Hashing  "+ str(result % p) + " = " + s)
	return result % p

# Computes a list of hashes for substrings length l, puts them in string_hashes[l]
def compute_string_hash(l):
	#print ("COMPUTING HASHES L " +  str(l))
	global answer
	b_pow_l_m_1 = powb(l-1)

	# This is the first case, do a sum
	suml = forcehash(compressed_log[:l])
	v = bug_hashes.get(suml)
	if v:
		answer += v

	for char_index in range(1, log_length-l + 1):
		rem = hash_letter_m(compressed_log[char_index - 1], b_pow_l_m_1)
		add = ord(compressed_log[char_index+ l - 1]) - 64
		#print ("Index is: " + str(char_index) + " Character is:" + compressed_log[char_index] + " Remove: " + str(rem) + " Add: " + str(add) )
		#print (suml)
		suml = ((suml - rem)*b + add) % p
		
		v = bug_hashes.get(suml)
		if v:
			answer += v

# Create bugs
for b_index in range (bug_length):
	bug = raw_input()
	h = forcehash(bug)

	v = bug_hashes.get(h)
	if not v:
		bug_hashes[h] = 1
	else:
		bug_hashes[h] = v + 1
	if len(bug) not in bugs_len:
		bugs_len.add(len(bug))



# Compare bug hashes to string hashes
for bl in bugs_len:
	compute_string_hash(bl)

# Debug
"""
print (string_hashes)
print (bugs)
print (bug_hashes)
print (compressed_log)
"""
print (answer)
