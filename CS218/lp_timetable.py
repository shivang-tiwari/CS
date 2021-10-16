# Name - Shivang Tiwari
# Roll number - 190040112
# Course - CS218
# Language - Python3
########################################################################################
import pulp as p 
########################################################################################
# Taking input and making the conflict graph
S = int(input())
inp = list(map(int,input(). split()))
R = inp[0]
cap = inp[1:]
C = int(input())
students = [None] * C
course_names = [None] * C
graph = []
for i in range(C):
	graph.append([])
for i in range(C):
	inp = input().split()
	students[i] = inp[2:]
	course_names[i] = inp[0]
for i in range(C):
	for j in range(i+1,C):
		for student in students[i]:
			if student in students[j]:
				graph[i].append(j)
				graph[j].append(i)
				break
########################################################################################
# Create a LP Maximization problem 
Lp_prob = p.LpProblem('MISProblem', p.LpMaximize)  
# Create problem Variables  
x = []
for i in range(C):
	grid = []
	for j in range(R):
		row = []
		for k in range(S):
			row.append(p.LpVariable("x"+str(i)+str(j)+str(k), cat = 'Binary'))
		grid.append(row)
	x.append(grid)
########################################################################################
# Objective Function 
allsum = 0
for i in range(C):
	for j in range(R):
		for k in range(S):
			allsum += x[i][j][k]
Lp_prob += allsum
########################################################################################
# Constraints
# Exactly One slot and one room for each course
for i in range(C):
	allsum = 0
	for j in range(R):
		for k in range(S):
			allsum += x[i][j][k]
	Lp_prob += allsum == 1

# No two courses in the same slot and same room
for j in range(R):
	for k in range(S):
		allsum = 0
		for i in range(C):
			allsum += x[i][j][k]
		Lp_prob += allsum <= 1

# Courses with common students must be in different slots
for k in range(S):
	for i in range(C):
		for y in graph[i]:
			allsum = 0
			for j in range(R):
				allsum += x[i][j][k] + x[y][j][k]
			Lp_prob += allsum <= 1
			
########################################################################################
print(Lp_prob)
status = Lp_prob.solve()   # Solver 
print(p.LpStatus[status])   # The solution status 
# Print the final solution 
for i in range(C):
	for j in range(R):
		for k in range(S):
			if(x[i][j][k].value() == 1):
				print("Schedule " + course_names[i] + " in slot " + str(k+1) + " and room " + str(j+1))
########################################################################################
