#include <iostream>
#include <vector>
#include <cstring>

std::vector<std::vector<int>> generate_variables(const int& n) {
    std::vector<std::vector<int>> variables;

    for (int i = 0; i < n; i++) {
        std::vector<int> row;
        for (int j = 0; j < n; j++) {
            row.push_back(i * n + j + 1); //Value in position (i, j) is (i * n + j + 1)
        }
        variables.push_back(row);
    }
    return variables;
}

void atMostOne(std::vector<std::vector<int>>& clauses, const std::vector<int>& variables) {
    for (int i = 0; i < variables.size(); i++) {
        for (int j = i + 1; j < variables.size(); j++) {
            std::vector<int> temp = {-variables[i], -variables[j]};
            clauses.push_back(temp);
        }
    }
}

void exactlyOne(std::vector<std::vector<int>>& clauses, const std::vector<int>& variables) {
    //At least a true value in variables
    clauses.push_back(variables);

    //Only one true value in variables
    atMostOne(clauses, variables);
}

std::vector<std::vector<int>> generate_clauses(const int& n, 
                                               const std::vector<std::vector<int>>& variables) {
    std::vector<std::vector<int>> clauses = {};

    //Exactly one queen in a row
    for (int i = 0; i < n; i++) {
        exactlyOne(clauses, variables[i]);
    }

    //Exactly one queen in a column
    for (int j = 0; j < n; j++) {
        std::vector<int> col;
        for (int i = 0; i < n; i++) {
            col.push_back(variables[i][j]);
        }
        exactlyOne(clauses, col);
    }

    //Only one queen in each diagonal
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 1; k < n; k++) {
                if (i + k < n && j + k < n) {
                    atMostOne(clauses, {variables[i][j], variables[i + k][j + k]});
                }
                if (i + k < n && j - k >= 0) {
                    atMostOne(clauses, {variables[i][j], variables[i + k][j - k]});
                }
            }
        }
    }
    return clauses;
}

void Solve() {
    int n = 5;
    std::vector<std::vector<int>> variables = generate_variables(n);
    std::vector<std::vector<int>> clauses = generate_clauses(n, variables);

    for (const auto& clause : clauses) {
        std::cout << "[";
        for (const auto& i : clause) {
            std::cout << i << " ";
        }
        std::cout << "0]\n";
    }
}

int main() {
    Solve();
    return 0;
}