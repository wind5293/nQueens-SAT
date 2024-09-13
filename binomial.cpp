#include <iostream>
#include <vector>
#include <cstring>

std::vector<std::vector<int>> generate_variables(const int& n) {
    std::vector<std::vector<int>> variables;

    for (int i = 0; i < n; i++) {
        std::vector<int> row;
        for (int j = 0; j < n; j++) {
            row.push_back(i * n + j + 1);
        }
        variables.push_back(row);
    }
    return variables;
}

void atMostOne(std::vector<std::vector<int>>& clauses, const std::vector<int>& variables) {
    for (int i = 0; i < variables.size(); i++) {
        for (int j = i + 1; j < variables.size(); j++) {
            std::vector<int> temp = {-variables[i], variables[j]};
            clauses.push_back(temp);
        }
    }
}

void exactlyOne()

void Solve() {
    int n = 5;
    std::vector<std::vector<int>> variables = generate_variables(n);

    for (int i = 0; i < n; i++) {
        
    }
}

int main() {
    Solve();
    return 0;
}