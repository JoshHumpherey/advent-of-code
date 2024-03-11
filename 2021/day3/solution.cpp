#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


vector<string> parseNumbers(const string& filePath) {
    ifstream inputFile(filePath);
    vector<string> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return lines;
    }
    string line;
    while (getline(inputFile, line)) {
        lines.push_back(line);
    }
    inputFile.close();
    return lines;
}

tuple<string, string> getDominantBits(const vector<string>& numbers) {
    string mostCommon { "" };
    string leastCommon { "" };

    for (auto idx = 0; idx < numbers[0].size(); idx++) {
        int ones { 0 };
        int zeros { 0 };
        for (auto j = 0; j < numbers.size(); j++) {
            if (numbers[j][idx] == '1') {
                ones++;
            } else {
                zeros++;
            }
        }

        if (zeros > ones) {
            mostCommon.push_back('0');
            leastCommon.push_back('1');
        } else {
            mostCommon.push_back('1');
            leastCommon.push_back('0');
        }
    }

    return make_tuple(mostCommon, leastCommon);
}

int calculatePowerConsumption(const vector<string>& numbers) {
    auto [mostCommon, leastCommon] = getDominantBits(numbers);
    return stoi(mostCommon, nullptr, 2) * stoi(leastCommon, nullptr, 2);
}

string getOxygenRating(vector<string>& numbers) {
    vector<string> results = {};
    for (auto i = 0; i < numbers.size(); i++) {
        results.push_back(numbers[i]);
    }

    for (auto idx = 0; idx < numbers[0].size(); idx++) {
        char patternBit;
        int ones = 0;
        int zeros = 0;
        for (auto j = 0; j < results.size(); j++) {
            if (results[j][idx] == '1') {
                ones++;
            } else {
                zeros++;
            }
        }
        if (ones >= zeros) {
            patternBit = '1';
        } else {
            patternBit = '0';
        }

        vector<string> filteredResults = {};
        for (auto k = 0; k < results.size(); k++) {
            if (results[k][idx] == patternBit) {
                filteredResults.push_back(results[k]);
            } 
        }
        if (filteredResults.size() == 1) {
            return filteredResults[0];
        } else {
            results = filteredResults;
        }
    }
    return "";
}

string getScrubberRating(vector<string>& numbers) {
    vector<string> results = {};
    for (auto i = 0; i < numbers.size(); i++) {
        results.push_back(numbers[i]);
    }

    for (auto idx = 0; idx < numbers[0].size(); idx++) {
        char patternBit;
        int ones = 0;
        int zeros = 0;
        for (auto j = 0; j < results.size(); j++) {
            if (results[j][idx] == '1') {
                ones++;
            } else {
                zeros++;
            }
        }
        if (zeros <= ones) {
            patternBit = '0';
        } else {
            patternBit = '1';
        }

        vector<string> filteredResults = {};
        for (auto k = 0; k < results.size(); k++) {
            if (results[k][idx] == patternBit) {
                filteredResults.push_back(results[k]);
            } 
        }
        if (filteredResults.size() == 1) {
            return filteredResults[0];
        } else {
            results = filteredResults;
        }
    }
    return "";
}

int calculateLifeSupportRating(vector<string> numbers) {
    string oxygenRating = getOxygenRating(numbers);
    string scrubberRating = getScrubberRating(numbers);
    return stoi(oxygenRating, nullptr, 2) * stoi(scrubberRating, nullptr, 2);
}


int main() {
    vector<string> numbers = parseNumbers("input.txt");

    cout << "Part 1: " + to_string(calculatePowerConsumption(numbers)) << endl;
    cout << "Part 2: " + to_string(calculateLifeSupportRating(numbers)) << endl;
}