# Name - Shivang Tiwari
# Roll number - 190040112
# Course - CS218
# Language - Python3
########################################################################################
# Problem Statement - 
# Integer linear programming is used to make the institute timetable.
# In this exercise you will try a simplified version of it.
# The input has the following form (tentative):

# no-of-slots
# number-of-class-rooms room-capacity ...
# no of courses
# course-no no-of-attending-students name-of-student ...
# ...

# You are supposed to assign a slot and a room to each course such that
# courses having common students are scheduled in distinct slots.
# Further, a course should be scheduled in a room of capacity no smaller
# than its enrollment.

# For example, the input might be

# 2
# 2 3 4
# 4
# cs601 3 xxx yyy zzz
# cs602 4 xxx aaa bbb ccc
# cs603 2 ppp zzz
# cs604 4 mmm ppp qqq rrr

# This says there are 2 slots, 2 classrooms of capacity 3, 4, and 4
# courses with some number of students.  A timetable is feasible for
# these constraints.  In slot1 we schedule cs601 in room1 and cs604 in
# room2.  In slot2 we schedule cs603 in room1, cs602 in room2.

# You are supposed to use the pulp linear programming package in python,
# an example is given in lec19.mis.py.  It should be self explanatory
# and there is documentation on the net; however please raise queries on
# the discussion group in moodle or the general channel on teams.

# The general idea for solving such problems is typically using
# indicator variables and expressing constraints in terms of those.  In
# this case you may consider binary variables x_{crs}, which is 1 if
# course c is scheduled in room r and slot s and 0 otherwise.

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
