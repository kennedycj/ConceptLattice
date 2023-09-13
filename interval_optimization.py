import pulp
import numpy as np
import pandas as pd

parameters = pd.read_excel(".\\Intervals.xlsx", sheet_name='Parameters')

N = len(parameters.index) # number of intervals
L = 0 # lower bound
U = 10 # upper bound

for index, row in parameters.iterrows():
    print(f"{index} row : {row}")

# Create a linear programming problem
lp_problem = pulp.LpProblem("MaxAbsDifference", pulp.LpMinimize)

# Create decision variables x_1 to x_n with the specified bounds
x = {}  # Dictionary to store the variables

# have to map variables to interval names

#for i in range(0, N):
    # x[2 * i + 1] = pulp.LpVariable(f"{parameters[2 * i, parameters.columns.get_loc('Name')]}", lowBound=L)
    # x[2 * i + 2] = pulp.LpVariable(f"{parameters[2 * i, parameters.columns.get_loc('Name')]}", upBound=U)

for i in range(1, 2 * N + 1):
    if i % 2 == 1:  # If i is odd
        variable = pulp.LpVariable(f"x_{i}", lowBound=L)
    else:  # If i is even
        variable = pulp.LpVariable(f"x_{i}", upBound=U)
    x[i] = variable

# Define the absolute difference variable
sum_var = pulp.LpVariable('sum_var')
abs_sum_var = pulp.LpVariable('abs_sum_var')

# Define the objective function to maximize the absolute difference
#lp_problem += abs_diff, "Minimize Absolute Difference"
lp_problem += abs_sum_var

odd_starts = []
for i in range(1, 2 * N + 1):
    for j in range(i, 2 * N + 1):
        if i % 2 == 1 and j % 2 == 1 and i != j:
            odd_starts.append((i, j))
            # sub_sum += (x[j] - x[i])
            print(f"i {i} j {j} ({x[j]} - {x[i]})")

def start_end(i, j):
    return (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1) and i != j and np.abs(i - j) > 1

for i in range(1, 2 * N + 1):
    for j in range(1, 2 * N + 1):
        if i % 2 == 1 and j % 2 == 0 and j != i + 1:
            # odd_starts.append((i, j))
            print(f"i {i} j {j} ({x[j]} - {x[i]})")

#print(odds)
for i, (a, b) in enumerate(odd_starts):
    print(f" a {a} b {b}")

w = [0.1, 0.3, 0.56, -0.4, 1, 0.2]

lp_problem += sum_var == pulp.lpSum([(x[a] - x[b]) for i, (a, b) in enumerate(odd_starts)])
lp_problem += abs_sum_var >= sum_var
lp_problem += abs_sum_var >= -sum_var
# Add constraints to the problem
z1 = pulp.LpVariable("z1", cat=pulp.LpBinary)
z2 = pulp.LpVariable("z2", cat=pulp.LpBinary)

M = 1000  # A large positive constant
m = 2

# x5 <= x3 <= x6
lp_problem += x[3] - x[6] <= M * (1 - z1)
lp_problem += x[5] - x[3] <= M * z1
# with fixed overlap when z1 = 1
lp_problem += x[6] - x[3] <= m * z1 + M * (1 - z1)
lp_problem += x[6] - x[3] >= m * z1 - M * (1 - z1)
# otherwise: x3 <= x5 <= x4 with fixed overlap when z2 = 1
lp_problem += x[3] - x[5] <= M * (1 - z2)
lp_problem += x[5] - x[4] <= M * z2
# with fixed overlap when z2 = 1
lp_problem += x[4] - x[5] <= m * z2 + M * (1 - z2)
lp_problem += x[4] - x[5] >= m * z2 - M + (1 - z2)

lp_problem += z1 + z2 == 1

# The lengths of the intervals
lp_problem += x[2] - x[1] == 4
lp_problem += x[4] - x[3] == 5
lp_problem += x[6] - x[5] == 6
# lp_problem += x[8] - x[7] == 2

# Interval start and end constraints (eg time intervals)
#lp_problem += x[4] == 10 # fixed end
#lp_problem += x[1] == 0 # fixed start
#lp_problem += x[1] - x[3] <= -5 # fixed distance between x1 and x3
#lp_problem += x[3] - x[2] == 1
#lp_problem += x[8] - x[2] <= -2

# Required minimum overlap

# Solve the linear programming problem
lp_problem.solve()

# Print the results
if pulp.LpStatus[lp_problem.status] == "Optimal":
    print("Optimal Solution:")
    for i in range(1, 2 * N + 1):
        print(f"x{i} = {x[i].varValue}")

    print(f"z1 {z1.varValue} z2 {z2.varValue}")
    print(f"abs_sum_var = {abs_sum_var.varValue}")
else:
    print("No optimal solution found.")
