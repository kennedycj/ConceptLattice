import pulp
import pandas as pd
import numpy as np
from enum import Enum

class Objective(Enum):
    MIN_START = 1
    MIN_END = 2
    MIN_LENGTH = 3
    MIN_DISTANCE = 4
class Optimizer:
    def __init__(self, number_of_intervals, lower_bound, upper_bound):

        O = pd.read_excel(".\\Intervals.xlsx", sheet_name='Overlap')

        self.no_reverse = True
        self.objective = Objective['MIN_DISTANCE']

        self.N = number_of_intervals
        M = 1000


        self.intervals = {}
        self.index = 0

        self.model = pulp.LpProblem(f"{self.objective.name}", pulp.LpMinimize)

        # Will eventually come from file of intervals: name, start, end
        # c_name = ['x_1', 'x_2', 'x_3']
        self.L = lower_bound

        self.U = upper_bound

        self.names = {}

        # Define the decision variables
        #self.C = [pulp.LpVariable(f"x_{i}", lowBound=self.L, upBound=self.U) for i in range(0, 2 * self.N)]


        self.C = []


        #z1 = pulp.LpVariable(f"z_1", cat=pulp.LpBinary)
        #z2 = pulp.LpVariable(f"z_2", cat=pulp.LpBinary)
        self.Z = len(O)
        self.z = [pulp.LpVariable(f"z_{i}", cat=pulp.LpBinary) for i in range(0, 4 * self.Z)]
        for i, row in O.iterrows():

            #print(f"lpSum([{z[i]} for {i} in range({i * Z}, {i * Z + 4}]) == 1")
            self.model += pulp.lpSum([self.z[j] for j in range(i * 4, i * 4 + 4)]) == 1

            a = O.at[i, 'Name_1']
            b = O.at[i, 'Name_2']
            L = O.at[i, 'Length']

            if pd.notnull(L):

                print(f"{a} overlaps {b} by {L}")

                a_s = self.C[2 * self.names[a]]
                a_e = self.C[2 * self.names[a] + 1]
                b_s = self.C[2 * self.names[b]]
                b_e = self.C[2 * self.names[b] + 1]

                # Constraints
                print(f"z[{i} * 4] = {self.z[i * 4]}")
                self.model += (a_s <= b_s + M * (1 - self.z[i * 4]))  # Condition 1: a_s <= b_s
                self.model += (a_e <= b_e + M * (1 - self.z[i * 4]))  # Condition 1: a_e <= b_e
                #model += (a_e - b_s == L + M * (1 - z[i * 4]))
                self.model += a_e - b_s <= L * self.z[i * 4] + M * (1 - self.z[i * 4])
                self.model += a_e - b_s >= L * self.z[i * 4] - M * (1 - self.z[i * 4])
                print(f"z[{i} * 4 + 1] = {self.z[i * 4 + 1]}")
                self.model += (b_s <= a_s + M * (1 - self.z[i * 4 + 1]))  # Condition 2: b_s <= a_s
                self.model += (b_e <= a_e + M * (1 - self.z[i * 4 + 1]))  # Condition 2: b_e <= a_e
                #model += (b_e - a_s == L + M * (1 - z[i * 4 + 1]))  # Condition 2: b_e - a_s = L
                self.model += b_e - a_s <= L * self.z[i * 4 + 1] + M * (1 - self.z[i * 4 + 1])
                self.model += b_e - a_s >= L * self.z[i * 4 + 1] - M * (1 - self.z[i * 4 + 1])
                print(f"{b_s} <= {a_s} + {M} * (1 - {self.z[i * 4 + 2]})")
                print(f"{a_e} <= {b_e} + {M} * (1 - {self.z[i * 4 + 2]})")
                print(f"{a_e} - {a_s} <= {L} * {self.z[i * 4 + 2]} + {M} * ({1 - self.z[i * 4 + 2]})")
                print(f"{a_e} - {a_s} >= {L} * {self.z[i * 4 + 2]} - {M} * ({1 - self.z[i * 4 + 2]})")
                self.model += (b_s <= a_s + M * (1 - self.z[i * 4 + 2]))  # Condition 3: b_s <= a_s
                self.model += (a_e <= b_e + M * (1 - self.z[i * 4 + 2]))  # Condition 3: a_e <= b_e
                self.model += a_e - a_s <= L * self.z[i * 4 + 2] + M * (1 - self.z[i * 4 + 2])
                self.model += a_e - a_s >= L * self.z[i * 4 + 2] - M * (1 - self.z[i * 4 + 2])
                print(f"z[{i} * 4 + 3] = {self.z[i * 4 + 3]}")
                self.model += (a_s <= b_s + M * (1 - self.z[i * 4 + 3]))  # Condition 4: a_s <= b_s
                self.model += (b_e <= a_e + M * (1 - self.z[i * 4 + 3]))  # Condition 4: b_e <= a_e
                #model += (b_e - b_s == L + M * (1 - z[i * 4 + 3]))  # Condition 4: b_e - b_s = L
                self.model += b_e - b_s <= L * self.z[i * 4 + 3] + M * (1 - self.z[i * 4 + 3])
                self.model += b_e - b_s >= L * self.z[i * 4 + 3] - M * (1 - self.z[i * 4 + 3])

    def check_interval_exists(self, name):
        if not name in self.intervals:
            self.intervals[name] = self.index
            self.C.extend([pulp.LpVariable(f"x_{i}", lowBound=self.L, upBound=self.U) for i in range(2 * self.index, 2 * self.index + 2)])
            print(f"name = {name} C = {self.C}")
            self.index += 1
    def add_interval(self, name, start=None, end=None, length=None):
        if not name in self.intervals:
            self.intervals[name] = self.index
            self.C.extend([pulp.LpVariable(f"x_{i}", lowBound=self.L, upBound=self.U) for i in range(2 * self.index, 2 * self.index + 2)])
            print(f"name = {name} C = {self.C}")
            self.index += 1

        if pd.notnull(start):
            self.model += self.C[2 * self.intervals[name]] == start

        if pd.notnull(end):
            self.model += self.C[2 * self.intervals[name] + 1] == end

        if pd.notnull(length):
            self.model += self.C[2 * self.intervals[name] + 1] - self.C[2 * self.intervals[name]] == length

    def solve(self):
        # By default, constrain intervals to have positive length: start <= end
        if self.no_reverse:
            for i in range(0, 2 * self.N, 2):
                self.model += self.C[i] <= self.C[i + 1]
        # Define the absolute difference variable
        self.sum = pulp.LpVariable('sum')
        self.abs_sum = pulp.LpVariable('abs_sum')

        if self.objective == Objective.MIN_DISTANCE:
            # Define the objective function to minimize the absolute difference
            self.model += self.sum == pulp.lpSum([pulp.lpSum([self.C[i] - self.C[j]] for j in range(i, 2 * self.N)) for i in range(0, 2 * self.N)])
            self.model += self.abs_sum >= self.sum
            self.model += self.abs_sum >= -self.sum
        # Solve the linear programming problem
        self.model.solve()

        # Print the results
        if pulp.LpStatus[self.model.status] == "Optimal":
            print("Optimal Solution:")
            for i in range(0, 2 * self.N):
                print(f"{self.C[i].name} = {self.C[i].varValue}")

            for i in range(0, 4 * self.Z):
                print(f"{self.z[i].name} = {self.z[i].varValue}")

            print(f"abs_sum_var = {self.abs_sum.varValue}")
        else:
            print("No optimal solution found.")

def optimize_from_file(filename):
    P = pd.read_excel(filename, sheet_name='Position')
    opt = Optimizer(len(P), 0, 10)
    # Define the intervals start, end, and length constraints
    names = opt.names
    for i, row in P.iterrows():
        name = P.at[i, 'Name']
        names[P.at[i, 'Name']] = i
        start = P.at[i, 'Start']
        end = P.at[i, 'End']
        length = P.at[i, 'Length']

        opt.add_interval(name, start, end, length)

    opt.solve()

if __name__ == '__main__':
    optimize_from_file(".\\Intervals.xlsx")