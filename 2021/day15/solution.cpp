#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>
#include <set>

using namespace std;

vector<vector<int>> getGrid(const string& filePath) {
    ifstream inputFile(filePath);
    vector<string> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return {};
    }
    string line;
    while (getline(inputFile, line)) {
        lines.push_back(line);
    }
    vector<vector<int>> grid = {};
    for (const auto& l : lines) {
        vector<int> row = {};
        for (auto c : l) {
            // Zero must be subtracted to account for ASCII conversion
            int val = c - '0';
            row.push_back(val);
        }
        grid.push_back(row);
    }
    return grid;
}

struct path {
    int cost;
    int r;
    int c;

    bool operator<(const path& other) const {
        return cost > other.cost;
    }
};

int lowestPathCost(vector<vector<int>> grid) {
    priority_queue<path> minHeap;
    minHeap.push(path{0, 0, 0});
    set<pair<int,int>> visited;

    while (!minHeap.empty()) {
        path p = minHeap.top();
        minHeap.pop();
        int totalCost = p.cost;
        int r = p.r;
        int c = p.c;
        visited.insert(make_pair(r,c));

        // cout << "evaluating r=" + to_string(r) + ", c=" + to_string(c) + ", cost=" + to_string(totalCost) << endl;
        if (r != 0 || c != 0) {
            totalCost += grid[r][c];
        }
        if (r == grid.size()-1 && c == grid[0].size()-1) {
            return totalCost;
        }
        path nextPaths[] = {
                {totalCost, r-1, c},
                {totalCost, r+1, c},
                {totalCost, r, c-1},
                {totalCost, r, c+1},
        };

        for (const path& nextP : nextPaths) {
            auto key = make_pair(nextP.r, nextP.c);
            if (nextP.r >= 0 && nextP.c >= 0 && nextP.r < grid.size() && nextP.c < grid[0].size() && visited.count(key) == 0) {
                minHeap.push(nextP);
            }
        }
    }
    return -1;
}


int main() {
    vector<vector<int>> grid = getGrid("input.txt");

    cout << "Part 1: " + to_string(lowestPathCost(grid)) << endl;
}