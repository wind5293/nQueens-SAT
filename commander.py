from pysat.solvers import Glucose3

def at_most_one(clauses, variables):
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

n = 6
variables = [1, 2, 3, 4, 5, 6]
