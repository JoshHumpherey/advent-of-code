#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

std::vector<std::string> splitString(const std::string& s, const std::string& delimiter) {
    std::vector<std::string> tokens;
    std::size_t pos = 0, found;

    while ((found = s.find(delimiter, pos)) != std::string::npos) {
        tokens.push_back(s.substr(pos, found - pos));
        pos = found + delimiter.size();
    }
    tokens.push_back(s.substr(pos)); // Add the last token
    return tokens;
}

struct reaction {
    string chain;
    map<string,string> insertMap;
};

reaction getPolymerInput(const string& filePath) {
    ifstream inputFile(filePath);
    vector<string> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return {};
    }
    reaction r;
    bool parsingInsertions = false;
    string line;
    while (getline(inputFile, line)) {
        if (line.empty()) {
            parsingInsertions = true;
        } else if (parsingInsertions) {
            auto pair = splitString(line, " -> ");
            r.insertMap[pair[0]] = pair[1];
        } else {
            r.chain = line;
        }
    }
    return r;
}

map<string,long> buildPolymerMap(string p) {
    map<string,long> polymerMap = {};
    for (long i = 0; i < p.size()-1; i++) {
        string key = p.substr(i, 2);
        if (polymerMap.count(key) > 0) {
            polymerMap[key] += 1;
        } else {
            polymerMap[key] = 1;
        }
    }
    return polymerMap;
}

map<string,long> advanceCycle(map<string,long> oldPolymer, map<string,string> insertMap) {
    map<string,long> newPolymer = {};
    for (const auto& pair : oldPolymer) {
        string key = pair.first;
        long amt = pair.second;
        string filler = insertMap[key];
        newPolymer[key[0] + filler] += amt;
        newPolymer[filler + key[1]] += amt;
    }
    return newPolymer;
}

long calculatePolymerScore(reaction r, long cycles) {
    auto polymerMap = buildPolymerMap(r.chain);
    for (auto i = 0; i < cycles; i++) {
        polymerMap = advanceCycle(polymerMap, r.insertMap);
    }
    map<string,long> scores = {};
    for (const auto& p : polymerMap) {
        scores[p.first.substr(0, 1)] += p.second;
        scores[p.first.substr(1, 1)] += p.second;
    }
    long maxCount = LONG_MIN;
    long minCount = LONG_MAX;
    for (const auto& s : scores) {
        if (s.second % 2 == 0) {
            scores[s.first] = scores[s.first] / 2;
        } else {
            scores[s.first] = (scores[s.first]+1) / 2;
        }

        if (scores[s.first] > maxCount) {
            maxCount = scores[s.first];
        }
        if (scores[s.first] < minCount) {
            minCount = scores[s.first];
        }
    }
    return maxCount - minCount;
}

int main() {
    reaction r = getPolymerInput("input.txt");

    cout << "Part 1: " + to_string(calculatePolymerScore(r, 10)) << endl;
    cout << "Part 2: " + to_string(calculatePolymerScore(r, 40)) << endl;
}