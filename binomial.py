def generate_variables(n):
    variables = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            variables[i].append(i * n + j + 1)
    return variables

def at_most_one(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses       

def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)

def generate_clauses(n, variables):
    clauses = []
    
    #Exacly one queen per rows
    for i in range(n):
        exactly_one(clauses, variables[i])
    
    #Exacly one queen per columns
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)])
        
    #At most one queen per diagonal
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j + k]])
                if i + k < n and j - k >= 0:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j - k]])
    return clauses
            
n = 3
variables = generate_variables(n)
clauses = generate_clauses(n, variables)
print(clauses)