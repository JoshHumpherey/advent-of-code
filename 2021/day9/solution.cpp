#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<vector<int>> getHeightMap(const string& filePath) {
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
    vector<vector<int>> heightMap = {};
    for (const auto& l : lines) {
        vector<int> row = {};
        for (auto c : l) {
            // Zero must be subtracted to account for ASCII conversion
            int val = c - '0';
            row.push_back(val);
        }
        heightMap.push_back(row);
    }
    return heightMap;
}

int getValue(vector<vector<int>> heightMap, int r, int c) {
    if (r >= heightMap.size() || c >= heightMap[0].size() || r < 0 || c < 0) {
        return INT_MAX;
    }
    return heightMap[r][c];
}

bool isLowPoint(vector<vector<int>> heightMap, int r, int c) {
    auto center = heightMap[r][c];
    auto up = getValue(heightMap, r-1, c);
    auto down = getValue(heightMap, r+1, c);
    auto left = getValue(heightMap, r, c-1);
    auto right = getValue(heightMap, r, c+1);
    return center < up && center < down && center < left && center < right;
}

int getRiskLevel(vector<vector<int>> heightMap) {
    int riskLevel = 0;
    for (auto r = 0; r < heightMap.size(); r++) {
        for (auto c = 0; c < heightMap[0].size(); c++) {
            if (isLowPoint(heightMap, r, c)) {
                riskLevel += (heightMap[r][c] + 1);
            }
        }
    }
    return riskLevel;
}


int main() {
    auto heightMap = getHeightMap("input.txt");

    cout << "Part 1: " + to_string(getRiskLevel(heightMap)) << endl;
}