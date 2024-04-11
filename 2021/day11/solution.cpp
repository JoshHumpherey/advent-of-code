#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <queue>
#include <set>

using namespace std;

const int FLASH_THRESHOLD = 10;

vector<vector<int>> getEnergyLevels(const string& filePath) {
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

void increase(vector<vector<int>>& energyLevels, set<pair<int,int>>& flashed, int r, int c) {
    if (r < 0 || c < 0 || r >= energyLevels.size() || c >= energyLevels[0].size() || flashed.count(make_pair(r,c))) {
        return;
    }
    energyLevels[r][c] += 1;
}

int flash(vector<vector<int>>& energyLevels) {
    queue<pair<int,int>> toFlash;
    set<pair<int,int>> flashed;

    for (auto r = 0; r < energyLevels.size(); r++) {
        for (auto c = 0; c < energyLevels[0].size(); c++) {
           energyLevels[r][c] += 1;
            if (energyLevels[r][c] >= FLASH_THRESHOLD) {
                toFlash.emplace(r,c);
            }
        }
    }
    while (!toFlash.empty()) {
        // process the current queue
        while (!toFlash.empty()) {
            pair<int, int> p = toFlash.front();
            toFlash.pop();
            int r = p.first;
            int c = p.second;
            increase(energyLevels, flashed, r-1, c-1);
            increase(energyLevels, flashed, r-1, c);
            increase(energyLevels, flashed, r-1, c+1);
            increase(energyLevels, flashed, r, c+1);
            increase(energyLevels, flashed, r+1, c+1);
            increase(energyLevels, flashed, r+1, c);
            increase(energyLevels, flashed, r+1, c-1);
            increase(energyLevels, flashed, r, c-1);
            energyLevels[r][c] = 0;
            flashed.insert(p);
        }
        // add to queue to determine if there are additional flashes that must happen
        for (auto r = 0; r < energyLevels.size(); r++) {
            for (auto c = 0; c < energyLevels[0].size(); c++) {
                auto p = make_pair(r,c);
                if (energyLevels[r][c] >= FLASH_THRESHOLD && flashed.count(p) == 0) {
                    toFlash.emplace(p);
                }
            }
        }
    }
    return flashed.size();
}

int getTotalFlashesAfterNSteps(vector<vector<int>> energyLevels, int n) {
    int flashes = 0;
    for (auto i = 0; i < n; i++) {
        flashes += flash(energyLevels);
    }
    return flashes;
}

int getFirstSynchronizedFlash(vector<vector<int>> energyLevels) {
    int flashed = 0;
    int cycles = 0;
    while (flashed != 100) {
        flashed = flash(energyLevels);
        cycles += 1;
    }
    return cycles;
}

int main() {
    auto energyLevels = getEnergyLevels("input.txt");

    cout << "Part 1: " + to_string(getTotalFlashesAfterNSteps(energyLevels, 100)) << endl;
    cout << "Part 2: " + to_string(getFirstSynchronizedFlash(energyLevels)) << endl;
}