from pysat.solvers import Glucose3

total_var_count = 0

def generate_variables(n):
    variables = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            variables[i].append(i * n + j + 1)
    return variables

def at_most_one(clauses, variables, new_var, n):
    clauses.append([-variables[0], new_var[0]])
    for i in range(1, len(variables) - 1):
        clauses.append([-variables[i], new_var[i]])
        clauses.append([-new_var[i - 1], new_var[i]])
        clauses.append([-new_var[i - 1], -variables[i]])
    clauses.append([-new_var[n - 2], -variables[n - 1]])

def exactly_one(clauses, variables, new_var, n):
    clauses.append(variables) # At least one
    at_most_one(clauses, variables, new_var, n)

def sequential_encoding(n, variables):
    clauses = []
    
    global total_var_count 
    total_var_count = n * n
    
    # Sequential in each row
    for i in range(len(variables)):
        temp_new_var = []
        for j in range(total_var_count + 1, total_var_count + n):
            temp_new_var.append(j)
        # print(temp_new_var)
        
        exactly_one(clauses, variables[i], temp_new_var, n)
        
        total_var_count += n - 1
    
    # Sequential in each column
    for i in range(n):
        temp_var = []
        for j in range(n):
            temp_var.append(variables[j][i])
        # print(temp_var)
        
        temp_new_var = []
        for j in range(total_var_count + 1, total_var_count + n):
            temp_new_var.append(j)
        
        exactly_one(clauses, temp_var, temp_new_var, n)
        total_var_count += + n - 1
        
    # Sequential in each diagonal
    # Diagonal with i - j = const
    for d in range(-n + 1, n):
        temp_var = []
        for i in range(n):
            j = i - d
            if i < n and 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            temp_new_var = [i for i in range(total_var_count + 1, total_var_count + len(temp_var))]
            total_var_count += len(temp_var) - 1
            at_most_one(clauses, temp_var, temp_new_var, len(temp_var))
            
    # Diagonal with i + j = const
    for d in range(2 * n - 1):
        temp_var = []
        for i in range(n):
            j = d - i
            if 0 <= j < n:
                temp_var.append(variables[i][j])
                
        if len(temp_var) > 1:
            temp_new_var = [i for i in range(total_var_count + 1, total_var_count + len(temp_var))]
            total_var_count += len(temp_var) - 1
            at_most_one(clauses, temp_var, temp_new_var, len(temp_var))   
                 
    return clauses

def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = sequential_encoding(n, variables)
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

n = 4
solution = solve_n_queens(n)
print_solution(solution)
