from pysat.solvers import Glucose3
import math

# Generate a matrix with n rows and n cols, base for a n * n board  
def generate_variables(n):
    variables = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            variables[i].append(i * n + j + 1)
    return variables

def generate_binary_combinations(n):
    binary = []
    for i in range(2 * n):
        binary.append(format(i, '0' + str(n) + 'b'))
    return binary

def generate_clauses(clauses, var, temp_clause):
    for i in range(len(temp_clause)):
        clauses.append([-var, temp_clause[i]])   

def binary_encoding(n, variables):
    new_variables = []
    for i in range(n + 1, n + 1 + math.ceil(math.log(n, 2))):
        new_variables.append(i) 
    # print(generate_new_variables)
    
    binary_combinations = generate_binary_combinations(len(new_variables))
    # print(binary_combinations)
    
    clauses = []
    clauses.append(variables)
    
    for i in range(len(variables)):
        combination = binary_combinations[i]
        temp_clause = []
        
        for j in range(len(combination) - 1, -1, -1):
            index = len(combination) - j - 1
            
            if combination[j] == '1':
                temp_clause.append(new_variables[index])
            elif combination[j] == '0':
                temp_clause.append(-new_variables[index])
        
        generate_clauses(clauses, variables[i], temp_clause)       
    
    print(clauses)

n = 5
variables = generate_variables(n)

binary_encoding(n, variables)