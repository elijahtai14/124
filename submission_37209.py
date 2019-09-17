n, m = map(int, raw_input().split())
sortedByTenacity = list(map(int, raw_input().split()))
majors = list(map(int, raw_input().split()))
"""
n = 5
m = 2
sortedByTenacity = [1,5,3,2,4]
majors = [1,2,1,2,1]
"""
peopleByMajor = []
mappingCount = 0
mapping = [-1] * (m+1)

# All the people
people = []
for i in range(0, n, 1):
	temp = [sortedByTenacity[i], majors[i]]
	people.append(temp) 


	if mapping[temp[1]] == -1:
		mapping[temp[1]] = mappingCount
		mappingCount += 1 
		peopleByMajor.append([temp])
	else:
		peopleByMajor[mapping[temp[1]]].append(temp)

#Solution counter
solutions = 0

def mergeSort(arr, p): 
	global solutions
	if len(arr) > 1:  
		left = arr[:len(arr)//2]  
		right= arr[len(arr)//2:]
		
		mergeSort(left, p) 
		mergeSort(right, p) 

		# Merge Left and Right
		leftindex = 0
		rightindex = 0
		largeindex = 0 
		while  rightindex < len(right) and leftindex < len(left): 
			if left[leftindex][0] > right[rightindex][0]: 
				if p:
					solutions += len(right) - rightindex
				else:
					solutions -= len(right) - rightindex
				#print (str(left[leftindex])+ " " +str(right[i]))
				arr[largeindex] = left[leftindex] 
				leftindex += 1
			else:	
				arr[largeindex] = right[rightindex] 
				
				rightindex += 1
			largeindex +=1

		while len(right) > rightindex:
			arr[largeindex] = right[rightindex] 
			rightindex += 1
			largeindex +=1
		while len(left) > leftindex: 
			arr[largeindex] = left[leftindex] 
			leftindex += 1
			largeindex +=1
          
		
mergeSort(people, True)
for array in peopleByMajor:
	mergeSort(array, False)
#print(people)
print(solutions)



