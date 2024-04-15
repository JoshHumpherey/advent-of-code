#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>
#include <set>

using namespace std;

vector<int> getIncrementedVector(const vector<int>& vec) {
    vector<int> incrementedVector = {};
    for (const int& v : vec) {
        auto val = v + 1;
        if (val > 9) {
            val = 1;
        }
        incrementedVector.push_back(val);
    }
    return incrementedVector;
}

vector<vector<int>> getExtendedGrid(const vector<vector<int>>& grid, int scaling) {
    vector<vector<int>> extendedGrid = {};

    // extend the grid to contain all the original rows but with extended columns
    for (const auto & r : grid) {
        vector<vector<int>> rows = {};
        rows.push_back(r);
        for (auto s = 0; s < scaling-1; s++) {
            auto chunk = getIncrementedVector(rows[rows.size()-1]);
            rows.push_back(chunk);
        }

        vector<int> extendedRow = {};
        for (const auto& row : rows) {
            for (auto val : row) {
                extendedRow.push_back(val);
            }
        }
        extendedGrid.push_back(extendedRow);
    }

    // extend the columns downward according to the pattern
    vector<vector<vector<int>>> chunks = {};
    chunks.push_back(extendedGrid);
    for (auto s = 0; s < scaling-1; s++) {
        vector<vector<int>> nextChunk = {};
        for (const auto& chunk : chunks[chunks.size()-1]) {
            nextChunk.push_back(getIncrementedVector(chunk));
        }
        chunks.push_back(nextChunk);
    }
    for (int i = 1; i < chunks.size(); i++) {
        for (const auto& row : chunks[i]) {
            extendedGrid.push_back(row);
        }
    }

    return extendedGrid;
}

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

        if (visited.count(make_pair(r,c)) > 0) {
            continue;
        }
        visited.insert(make_pair(r,c));

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
    auto grid = getGrid("input.txt");
    auto extendedGrid = getExtendedGrid(grid, 5);
    
    cout << "Part 1: " + to_string(lowestPathCost(grid)) << endl;
    cout << "Part 2: " + to_string(lowestPathCost(extendedGrid)) << endl;
}