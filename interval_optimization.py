import pulp
import numpy as np
import pandas as pd

parameters = pd.read_excel(".\\Intervals.xlsx", sheet_name='Parameters')

x = {} # decision variables
model = pulp.LpProblem("MaxAbsDifference", pulp.LpMinimize)

N = len(parameters.index) # number of intervals
L = 0 # lower bound
U = 10 # upper bound
M = 1000  # A large positive constant

for index, row in parameters.iterrows():
    print(f"{index} row : {row}")



# Create decision variables x_1 to x_n with the specified bounds


# have to map variables to intervals names

positions = pd.DataFrame(columns=['Name', 'Start', 'End'])

for i in range(0, N):
    interval_column = parameters.columns.get_loc('Name')
    interval_row = 2 * i
    start_index = interval_row + 1
    end_index = interval_row + 2
    print(f"interval_name = parameters[{i}, {interval_column}]")
    interval_name = parameters.at[i, 'Name']
    x[start_index] = pulp.LpVariable(f"x_{start_index}", lowBound=L)
    x[end_index] = pulp.LpVariable(f"x_{end_index}", upBound=U)

    row = pd.DataFrame([{'Name': interval_name, 'Start': x[start_index], 'End' : x[end_index]}], index=[0])
    positions = pd.concat([positions, row], ignore_index=True)
    # x[2 * i + 1] = pulp.LpVariable(f"{parameters[2 * i, parameters.columns.get_loc('Name')]}", lowBound=L)
    # x[2 * i + 2] = pulp.LpVariable(f"{parameters[2 * i, parameters.columns.get_loc('Name')]}", upBound=U)

z = {}
z_index = 1
for i, row in positions.iterrows():
    # The intervals length constraints
    model += positions.at[i, 'End'] - positions.at[i, 'Start'] == parameters.at[i, 'Length']

    # Add overlap constraints
    partner = parameters.at[i, 'Overlaps With']
    if not pd.isnull(partner):
        print(f"partner = {partner}")
        m = parameters.at[i, 'By Amount']
        z[z_index] = pulp.LpVariable(f"z_{z_index}", cat=pulp.LpBinary)
        z1 = z[z_index]
        z_index += 1
        z[z_index] = pulp.LpVariable(f"z_{z_index}", cat=pulp.LpBinary)
        z2 = z[z_index]
        z_index += 1

        # x5 <= x3 <= x6
        # lp_problem += x[3] - x[6] <= M * (1 - z1)
        # lp_problem += x[5] - x[3] <= M * z1
        # with fixed overlap when z1 = 1
        print(f"[i] = {positions[positions['Name'] == partner]}")
        print(f"[j] = {positions.columns.get_loc('End')}")
        x_e = positions[positions['Name'] == partner].iat[0, positions.columns.get_loc('End')]
        print(f"x_e : {x_e}")
        x_s = positions.at[i, 'Start']
        print(f"x_s : {x_s}")
        overlap = pulp.LpAffineExpression([(x_e, 1), (x_s, -1)])
        print(f"{overlap}")
        #print(f"overlap expression = {overlap}")
        #overlap = LpAffineExpression([(x[0], 1), (x[1], -3), (x[2], 4)])
        #print(f"overlap = {positions[positions['Name'] == partner]['End'] - positions.at[i, 'Start']}")
        # x5 <= x3 <= x6 <-- SEE IF WE CAN DELETE THIS CONSTRAINT
        #model += x[3] - x[6] <= M * (1 - z1)
        #model += x[5] - x[3] <= M * z1
        # with fixed overlap when z1 = 1
        model += overlap <= m * z1 + M * (1 - z1)
        model += overlap >= m * z1 - M * (1 - z1)
        # otherwise: x3 <= x5 <= x4 with fixed overlap when z2 = 1
        #model += x[3] - x[5] <= M * (1 - z2)
        #model += x[5] - x[4] <= M * z2
        # with fixed overlap when z2 = 1
        x_s = positions.at[i, 'End']
        x_e = positions[positions['Name'] == partner].iat[0, positions.columns.get_loc('Start')]
        overlap = pulp.LpAffineExpression([(x_e, -1), (x_s, 1)])
        print(f"{overlap}")
        model += overlap <= m * z2 + M * (1 - z2)
        model += overlap >= m * z2 - M + (1 - z2)

        model += z1 + z2 == 1
        #lp_problem += x[2] - x[1] == 4
        #lp_problem += x[4] - x[3] == 5
        #lp_problem += x[6] - x[5] == 6

#for i in range(1, 2 * N + 1):
#   if i % 2 == 1:  # If i is odd
#        variable = pulp.LpVariable(f"x_{i}", lowBound=L)
#    else:  # If i is even
#        variable = pulp.LpVariable(f"x_{i}", upBound=U)
#    x[i] = variable

# Define the absolute difference variable
sum_var = pulp.LpVariable('sum_var')
abs_sum_var = pulp.LpVariable('abs_sum_var')

# Define the objective function to maximize the absolute difference
#lp_problem += abs_diff, "Minimize Absolute Difference"
#model += abs_sum_var

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

model += sum_var == pulp.lpSum([(x[a] - x[b]) for i, (a, b) in enumerate(odd_starts)])
model += abs_sum_var >= sum_var
model += abs_sum_var >= -sum_var


# lp_problem += x[8] - x[7] == 2

# Interval start and end constraints (eg time intervals)
model += x[4] == 10 # fixed end
model += x[5] == 2
#lp_problem += x[1] == 0 # fixed start
#lp_problem += x[1] - x[3] <= -5 # fixed distance between x1 and x3
#lp_problem += x[3] - x[2] == 1
#lp_problem += x[8] - x[2] <= -2

# Required minimum overlap

# Solve the linear programming problem
model.solve()

# Print the results
if pulp.LpStatus[model.status] == "Optimal":
    print("Optimal Solution:")
    for i in range(1, 2 * N + 1):
        print(f"x{i} = {x[i].varValue}")

    for i, row in positions.iterrows():
        print(f"interval {positions.at[i, 'Name']} {positions.at[i, 'Start'].varValue} {positions.at[i, 'End'].varValue}")

    for i in range(1, z_index):
        print(f"z1_{i} = {z[i].varValue}")

    print(f"abs_sum_var = {abs_sum_var.varValue}")
else:
    print("No optimal solution found.")
