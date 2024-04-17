#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cctype>

using namespace std;

const long long SIM_COUNT = 500;

vector<string> splitString(const std::string& s, const std::string& delimiter) {
    vector<std::string> tokens;
    size_t pos = 0, found;
    while ((found = s.find(delimiter, pos)) != std::string::npos) {
        tokens.push_back(s.substr(pos, found - pos));
        pos = found + delimiter.size();
    }
    tokens.push_back(s.substr(pos)); // Add the last token
    return tokens;
}

struct target {
    int x[2];
    int y[2];
};

target getTarget(const string& filePath) {
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
    auto rawPairs = splitString(splitString(lines[0], ": ")[1], ", ");
    auto rawXPair = splitString(splitString(rawPairs[0], "x=")[1], "..");
    auto rawYPair = splitString(splitString(rawPairs[1], "y=")[1], "..");
    return target {
        {stoi(rawXPair[0]), stoi(rawXPair[1])},
        {stoi(rawYPair[0]), stoi(rawYPair[1])},
    };
}

struct simResult {
    bool hit;
    long long maxHeight;
};

simResult simulateProbeShot(long long x, long long y, target t) {
    long long pos[] = {0, 0};
    long long vel[] = {x, y};
    long long maxHeight = LLONG_MIN;
    while (true) {
        pos[0] += vel[0];
        pos[1] += vel[1];
        maxHeight = max(pos[1], maxHeight);
        if (t.x[0] <= pos[0] && pos[0] <= t.x[1] && t.y[0] <= pos[1] && pos[1] <= t.y[1]) {
            return simResult{true, maxHeight};
        } else if (pos[1] < t.y[0]) {
            return simResult{false, -1};
        }

        vel[0] = max(vel[0]-1, 0ll);
        vel[1] -= 1;
    }
}

struct simulations{
    long long successfulLaunches;
    long long maxHeight;
};

simulations runProbeSimulations(const target& t) {
    long long maxHeight = LLONG_MIN;
    long long successfulLaunches = 0;

    for (auto x = 1; x <= SIM_COUNT; x++) {
        for (auto y = -500; y <= SIM_COUNT; y++) {
            auto res = simulateProbeShot(x, y, t);
            if (res.hit) {
                successfulLaunches += 1;
                maxHeight = max(maxHeight, res.maxHeight);
            }
        }
    }
    return simulations{successfulLaunches, maxHeight};
}

int main() {
    auto target = getTarget("input.txt");
    auto sims = runProbeSimulations(target);

    cout << "Part 1: " + to_string(sims.maxHeight) << endl;
    cout << "Part 2: " + to_string(sims.successfulLaunches) << endl;
}