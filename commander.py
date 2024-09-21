from pysat.solvers import Glucose3
import math

total_var_count = 0

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def grouping_variables(variables, var_per_group):
    groups = []
    temp_group = []
    for i in range(len(variables)):
        temp_group.append(variables[i])
        if (i + 1) % var_per_group == 0 or i + 1 == len(variables):
            groups.append(temp_group)
            temp_group = []
    return groups

def binomial_AMO(clauses, variables):
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

def binomial_EO(clauses, variables):
    clauses.append(variables)
    binomial_AMO(clauses, variables)
    
def at_most_one(clauses, variables):
    n = len(variables)
    global total_var_count
    total_var_count += len(variables)
    
    groups = grouping_variables(variables, math.ceil(n / math.floor(math.sqrt(n))))
    # print(groups)
    commanders = [i for i in range(total_var_count + 1, total_var_count + len(groups) + 1)]
    # print(commanders)
    total_var_count += len(commanders)
    
    binomial_EO(clauses, commanders)
    for i in range(len(commanders)):
        clauses.append([-commanders[i]] + groups[i])
        binomial_AMO(clauses, groups[i])
        
        for j in range(len(groups[i])):
            clauses.append([-commanders[i], -groups[i][j]])
    
def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)

def generate_clauses(n, variables):
    clauses = []
    
    global total_var_count
    total_var_count = n * n
    
    for i in range(n):
        exactly_one(clauses, variables[i])
    
    for j in range(n):
        temp_var = []
        for i in range(n):
            temp_var.append(variables[i][j])
        exactly_one(clauses, temp_var)
    
    # Diagonal with i - j = const
    for d in range(-n + 1, n):
        temp_var = []
        for i in range(n):
            j = i - d
            if i < n and 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            at_most_one(clauses, temp_var)
            
            
    # Diagonal with i + j = const
    for d in range(2 * n - 1):
        temp_var = []
        for i in range(n):
            j = d - i
            if 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            at_most_one(clauses, temp_var)
             
    return clauses    
    
def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)
    print(clauses)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None
            
def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        print(solution)
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row)) 
        
n = 5
solution = solve_n_queens(n)
print_solution(solution)
