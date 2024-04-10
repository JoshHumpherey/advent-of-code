#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

const int PEAK = 9;

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

vector<pair<int,int>> getLowPoints(vector<vector<int>> heightMap) {
    vector<pair<int,int>> lowPoints = {};
    for (auto r = 0; r < heightMap.size(); r++) {
        for (auto c = 0; c < heightMap[0].size(); c++) {
            if (isLowPoint(heightMap, r, c)) {
                lowPoints.emplace_back(r,c);
            }
        }
    }
    return lowPoints;
}

int getRiskLevel(vector<pair<int,int>> lowPoints, vector<vector<int>> heightMap) {
    int riskLevel = 0;
    for (auto p : lowPoints) {
        riskLevel += heightMap[p.first][p.second] + 1;
    }
    return riskLevel;
}

int expand(vector<vector<int>>& heightMap, int lastVal, int r, int c) {
    if (r < 0 || c < 0 || r >= heightMap.size() || c >= heightMap[0].size() || heightMap[r][c] == PEAK || heightMap[r][c] <= lastVal) {
        return 0;
    }
    lastVal = heightMap[r][c];
    heightMap[r][c] = PEAK;
    int flooded = 1;
    flooded += expand(heightMap, lastVal, r+1, c);
    flooded += expand(heightMap, lastVal, r-1, c);
    flooded += expand(heightMap, lastVal, r, c+1);
    flooded += expand(heightMap, lastVal, r, c-1);
    return flooded;
}

vector<int> getBasinSizes(vector<pair<int,int>> lowPoints, vector<vector<int>> heightMap) {
    map<pair<int,int>,int> seen = {};
    vector<int> basinSizes = {};

    for (auto p : lowPoints) {
        auto localSize = expand(heightMap, INT_MIN, p.first, p.second);
        basinSizes.push_back(localSize);
    }
    sort(basinSizes.begin(), basinSizes.end());
    return basinSizes;
}

int getTopLargestBasins(vector<pair<int,int>> lowPoints, vector<vector<int>> heightMap) {
    auto basinSizes = getBasinSizes(lowPoints, heightMap);
    auto endIdx = basinSizes.size()-1;
    return basinSizes[endIdx] * basinSizes[endIdx-1] * basinSizes[endIdx-2];
}


int main() {
    auto heightMap = getHeightMap("input.txt");
    auto lowPoints = getLowPoints(heightMap);

    cout << "Part 1: " + to_string(getRiskLevel(lowPoints, heightMap)) << endl;
    cout << "Part 2: " + to_string(getTopLargestBasins(lowPoints, heightMap)) << endl;
}