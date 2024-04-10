#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<int> getCrabPositions(const string& filePath) {
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

    vector<int> crabPositions = {};
    char delim = ',';
    string temp;
    for (char i : lines[0]) {
        if (i == delim) {
            crabPositions.push_back(stoi(temp));
            temp = "";
        } else {
            temp.push_back(i);
        }
    }
    if (!temp.empty()) {
        crabPositions.push_back(stoi(temp));
    }
    sort(crabPositions.begin(), crabPositions.end());
    return crabPositions;
}

long long getMedianPosition(vector<int>& positions) {
    auto mid = positions.size() / 2;
    return positions[mid];
}

long long calculateConstantFuelToPoint(vector<int>& positions) {
    auto point = getMedianPosition(positions);
    long long fuel = 0;
    for (auto p : positions) {
        fuel += abs(p - point);
    }
    return fuel;
}

long long getAveragePosition(const vector<int>& positions) {
    long long total = 0;
    for (auto p : positions) {
        total += p;
    }

    return total / positions.size();
}

long long calculateIncreasingFuelToPoint(vector<int>& positions) {
    auto point = getAveragePosition(positions);
    long long fuel = 0;
    for (auto p : positions) {
        auto distance = abs(p - point);
        fuel += distance * (distance + 1) / 2;
    }
    return fuel;
}


int main() {
    auto crabPositions = getCrabPositions("input.txt");

    cout << "Part 1: " + to_string(calculateConstantFuelToPoint(crabPositions)) << endl;
    cout << "Part 2: " + to_string(calculateIncreasingFuelToPoint(crabPositions)) << endl;
}

