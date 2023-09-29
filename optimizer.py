import pulp
import pandas as pd
import portion as P
import draw
import matplotlib.pyplot as plt

class Optimizer:
    def __init__(self, lower_bound, upper_bound, no_reverse=True, limit=1000):
        self.no_reverse = no_reverse
        self.M = limit
        self.intervals = {}
        self.N = 0
        self.overlap_index = 0
        self.model = pulp.LpProblem(f"Maximum distance", pulp.LpMinimize)
        self.L = lower_bound
        self.U = upper_bound
        self.C = []
        self.z = []
        self.Z = 0
        # Define the absolute difference variable
        self.sum = pulp.LpVariable('sum')
        self.abs_sum = pulp.LpVariable('abs_sum')

    def add_interval(self, name, start=None, end=None, length=None):
        if not name in self.intervals:
            self.intervals[name] = self.N
            self.C.extend([pulp.LpVariable(f"x_{i}", lowBound=self.L, upBound=self.U) for i in range(2 * self.N, 2 * self.N + 2)])
            print(f"this = {name} C = {self.C}")
            self.N += 1

        if pd.notnull(start):
            self.model += self.C[2 * self.intervals[name]] == start

        if pd.notnull(end):
            self.model += self.C[2 * self.intervals[name] + 1] == end

        if pd.notnull(length):
            self.model += self.C[2 * self.intervals[name] + 1] - self.C[2 * self.intervals[name]] == length
    def add_interval_overlap(self, this, that, length):
        if not this in self.intervals or not that in self.intervals:
            raise TypeError('interval does not exist')

        self.z.extend([pulp.LpVariable(f"z_{i}", cat=pulp.LpBinary) for i in range(4 * self.Z, 4 * self.Z + 4)])
        self.model += pulp.lpSum([self.z[i] for i in range(4 * self.Z, 4 * self.Z + 4)]) == 1

        print(f"{this} overlaps {that} by {length}")
        a_s = self.C[2 * self.intervals[this]]
        a_e = self.C[2 * self.intervals[this] + 1]
        b_s = self.C[2 * self.intervals[that]]
        b_e = self.C[2 * self.intervals[that] + 1]

        # Constraints
        i = self.Z
        L = length
        print(f"z[{i} * 4] = {self.z[i * 4]}")
        self.model += (a_s <= b_s + self.M * (1 - self.z[i * 4]))  # Condition 1: a_s <= b_s
        self.model += (a_e <= b_e + self.M * (1 - self.z[i * 4]))  # Condition 1: a_e <= b_e
        # model += (a_e - b_s == L + M * (1 - z[i * 4]))
        self.model += a_e - b_s <= L * self.z[i * 4] + self.M * (1 - self.z[i * 4])
        self.model += a_e - b_s >= L * self.z[i * 4] - self.M * (1 - self.z[i * 4])
        print(f"z[{i} * 4 + 1] = {self.z[i * 4 + 1]}")
        self.model += (b_s <= a_s + self.M * (1 - self.z[i * 4 + 1]))  # Condition 2: b_s <= a_s
        self.model += (b_e <= a_e + self.M * (1 - self.z[i * 4 + 1]))  # Condition 2: b_e <= a_e
        # model += (b_e - a_s == L + M * (1 - z[i * 4 + 1]))  # Condition 2: b_e - a_s = L
        self.model += b_e - a_s <= L * self.z[i * 4 + 1] + self.M * (1 - self.z[i * 4 + 1])
        self.model += b_e - a_s >= L * self.z[i * 4 + 1] - self.M * (1 - self.z[i * 4 + 1])
        print(f"{b_s} <= {a_s} + {self.M} * (1 - {self.z[i * 4 + 2]})")
        print(f"{a_e} <= {b_e} + {self.M} * (1 - {self.z[i * 4 + 2]})")
        print(f"{a_e} - {a_s} <= {L} * {self.z[i * 4 + 2]} + {self.M} * ({1 - self.z[i * 4 + 2]})")
        print(f"{a_e} - {a_s} >= {L} * {self.z[i * 4 + 2]} - {self.M} * ({1 - self.z[i * 4 + 2]})")
        self.model += (b_s <= a_s + self.M * (1 - self.z[i * 4 + 2]))  # Condition 3: b_s <= a_s
        self.model += (a_e <= b_e + self.M * (1 - self.z[i * 4 + 2]))  # Condition 3: a_e <= b_e
        self.model += a_e - a_s <= L * self.z[i * 4 + 2] + self.M * (1 - self.z[i * 4 + 2])
        self.model += a_e - a_s >= L * self.z[i * 4 + 2] - self.M * (1 - self.z[i * 4 + 2])
        print(f"z[{i} * 4 + 3] = {self.z[i * 4 + 3]}")
        self.model += (a_s <= b_s + self.M * (1 - self.z[i * 4 + 3]))  # Condition 4: a_s <= b_s
        self.model += (b_e <= a_e + self.M * (1 - self.z[i * 4 + 3]))  # Condition 4: b_e <= a_e
        # model += (b_e - b_s == L + M * (1 - z[i * 4 + 3]))  # Condition 4: b_e - b_s = L
        self.model += b_e - b_s <= L * self.z[i * 4 + 3] + self.M * (1 - self.z[i * 4 + 3])
        self.model += b_e - b_s >= L * self.z[i * 4 + 3] - self.M * (1 - self.z[i * 4 + 3])

        self.Z += 1
    def add_interval_order(self, first, second, distance, starts=False):
        """
        Add distance constraint between two intervals, first and second. Assumes first is before second. If starts is
        True, ensure second.start is exactly distance (d) from first.start; otherwise, by default, second.start is
        exactly distance (d) from first.end.
        """
        if not first in self.intervals or not second in self.intervals:
            raise TypeError('interval does not exist')

        a_s = self.C[2 * self.intervals[first]]
        a_e = self.C[2 * self.intervals[first] + 1]
        b_s = self.C[2 * self.intervals[second]]

        if starts:
            self.model += (b_s - a_s) == distance
        else:
            self.model += (b_s - a_e) == distance
    def solve(self, normalize=False, scale=False):
        if scale:
            normalize = True
        # By default, constrain intervals to have positive length: start <= end
        if self.no_reverse:
            for i in range(0, 2 * self.N, 2):
                self.model += self.C[i] <= self.C[i + 1]

        # Define the objective function to minimize the absolute difference
        self.model += self.sum == pulp.lpSum([pulp.lpSum([self.C[i] - self.C[j]] for j in range(i, 2 * self.N)) for i in range(0, 2 * self.N)])
        self.model += self.abs_sum >= self.sum
        self.model += self.abs_sum >= -self.sum

        # Solve the linear programming problem
        self.model.solve()

        if normalize:
            max_x = (max(self.C, key=lambda x: x.varValue)).varValue
            min_x = (min(self.C, key=lambda x: x.varValue)).varValue

            shift = 0
            factor = 1
            if scale:
                shift = self.L
                factor = self.U - self.L

            for i in range(0, len(self.C)):
                self.C[i].varValue = shift + factor * (self.C[i].varValue - min_x) / (max_x - min_x)

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
    def as_intervals(self):
        return [P.open(self.C[i].varValue, self.C[i + 1].varValue) for i in range(0, len(self.C), 2)]

    def interval_names(self):
        return sorted(self.intervals, key=lambda k: self.intervals[k])
def optimize_from_file(filename, scale=False):
    P = pd.read_excel(filename, sheet_name='Position')
    O = pd.read_excel(".\\Intervals.xlsx", sheet_name='Overlap')
    opt = Optimizer(0, 10)
    # Define the intervals start, end, and length constraints
    names = {}
    for i, row in P.iterrows():
        name = P.at[i, 'Name']
        names[P.at[i, 'Name']] = i
        start = P.at[i, 'Start']
        end = P.at[i, 'End']
        length = P.at[i, 'Length']

        opt.add_interval(name, start, end, length)

    for i, row in O.iterrows():
        name = O.at[i, 'Name_1']
        partner = O.at[i, 'Name_2']
        length = O.at[i, 'Length']

        if pd.notnull(length):
            opt.add_interval_overlap(name, partner, length)

    opt.solve(scale=scale)
    return opt

if __name__ == '__main__':
    opt = optimize_from_file(".\\Intervals.xlsx", scale=True)
    print(f"intervals = {opt.as_intervals()}")
    # Plot
    draw.graph(RM=opt.as_intervals(), names=opt.interval_names(), lw=5, c='b')

    # Draw
    plt.show()