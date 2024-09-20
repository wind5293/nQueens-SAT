import math
from pysat.solvers import Glucose3

total_var_count = 0

def generate_variables(n):
    variables = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            variables[i].append(i * n + j + 1)
    return variables

def binomial_AMO(clauses, variables):
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

# At most one using product encoding
def at_most_one(clauses, n, variables): 
    p = math.ceil(math.sqrt(n))
    v = math.ceil(n / p)
    
    global total_var_count
    
    new_var_row = []
    for i in range(p):
        new_var_row.append(total_var_count + i + 1)
    total_var_count += p
    
    binomial_AMO(clauses, new_var_row)
    
    new_var_col = []
    for i in range(v):
        new_var_col.append(total_var_count + i + 1) 
    total_var_count += v
    
    binomial_AMO(clauses, new_var_col)
    
    for i in range(len(variables)):
        if math.ceil(i / v) == i / v:
            r = math.ceil(i / v)
        else:
            r = math.ceil(i / v) - 1
        c = i % v
        
        clauses.append([-variables[i], new_var_row[r]])
        clauses.append([-variables[i], new_var_col[c]])

def exactly_one(clauses, n, variables):
    clauses.append(variables)
    at_most_one(clauses, n, variables)

def generate_clauses(n, variables):
    clauses = []
    
    global total_var_count
    total_var_count = n * n
    
    for i in range(n):
        exactly_one(clauses, len(variables[i]), variables[i])
        
    for j in range(n):
        temp_var = []
        for i in range(n):
            temp_var.append(variables[i][j])
        exactly_one(clauses, len(temp_var), temp_var)
    
    
    # Sequential in each diagonal
    # Diagonal with i - j = const
    for d in range(-n + 1, n):
        temp_var = []
        for i in range(n):
            j = i - d
            if i < n and 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            at_most_one(clauses, len(temp_var), temp_var)
            
            
    # Diagonal with i + j = const
    for d in range(2 * n - 1):
        temp_var = []
        for i in range(n):
            j = d - i
            if 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            at_most_one(clauses, len(temp_var), temp_var)
             
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
