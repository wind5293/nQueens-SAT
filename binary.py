from pysat.solvers import Glucose3
import math

total_var_count = 0

def generate_variables(n):
    variables = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            variables[i].append(i * n + j + 1)
    return variables

def generate_binary_combinations(n):
    binary = []
    for i in range(2 ** n):
        binary.append(format(i, '0' + str(n) + 'b'))
    return binary

def binary_encoding(clauses, variables, temp_new_var):
    for i in range(len(temp_new_var)):
        clauses.append([-variables, temp_new_var[i]])

def at_most_one(clauses, variables):
    global total_var_count

    temp_new_var = [i for i in range(total_var_count + 1, total_var_count + math.ceil(math.log(len(variables), 2)) + 1)]
    total_var_count += len(temp_new_var)
    binary_combinations = generate_binary_combinations(len(temp_new_var)) 
    # print(binary_combinations)   
    
    for i in range(len(variables)):
        combination = binary_combinations[i]
        temp_clause = []
        for j in range(len(combination) - 1, -1, -1):
            ind = len(combination) - j - 1
            if combination[j] == '1':
                temp_clause.append(temp_new_var[ind])
            else: temp_clause.append(-temp_new_var[ind])
        
        binary_encoding(clauses, variables[i], temp_clause)
    
def exactly_one(clauses, variables):
    clauses.append(variables)      
    at_most_one(clauses, variables)
    
def generate_clauses(n, variables):
    clauses = []
    global total_var_count
    total_var_count = n * n
    # Exactly one queen in a row
    for i in range(n):
        exactly_one(clauses, variables[i])
    
    # Exactly one queen in a col
    for j in range(n):
        temp_var = []
        for i in range(n):
            temp_var.append(variables[i][j])
        exactly_one(clauses, temp_var)
    
    # Binary in each diagonal
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
