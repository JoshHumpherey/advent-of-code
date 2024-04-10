#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

class LanternFish {
private:
    map<int, long long> ages;
public:
    explicit LanternFish(const string& s) {
        char delim = ',';
        string temp;
        for (char i : s) {
            if (i == delim) {
                int key = stoi(temp);
                if (ages.count(key) > 0) {
                    ages[key] += 1;
                } else {
                    ages[key] = 1;
                }
                temp = "";
            } else {
                temp.push_back(i);
            }
        }
        if (!temp.empty()) {
            int key = stoi(temp);
            if (ages.count(key) > 0) {
                ages[key] += 1;
            } else {
                ages[key] = 1;
            }
        }
    }

    void AdvanceDay() {
        map<int, long long> newAges = {};
        long long recycledParents = 0;

        for (auto i = 0; i <= 8; i++) {
            int nextIdx = i-1;
            if (nextIdx < 0) {
                nextIdx = 8;
            }

            if (ages.count(i) > 0) {
                newAges[nextIdx] = ages[i];
                if (nextIdx == 8) {
                    recycledParents = ages[i];
                }
            } else {
                newAges[nextIdx] = 0;
            }
        }

        if (recycledParents > 0) {
            if (newAges.count(6) > 0) {
                newAges[6] += recycledParents;
            } else {
                newAges[6] = recycledParents;
            }
        }

        ages = newAges;
    }

    long long Total() {
        long long result = 0;
        for (auto pair : ages) {
            result += pair.second;
        }
        return result;
    }
};

string getRawLanternFish(const string& filePath) {
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
    return lines[0];
}

long long getTotalLanternFishCount(LanternFish l, int days) {
    for (auto i = 0; i < days; i++) {
        l.AdvanceDay();
    }
    return l.Total();
}


int main() {
    cout << "Part 1: " + to_string(getTotalLanternFishCount( LanternFish(getRawLanternFish("input.txt")), 80)) << endl;
    cout << "Part 2: " + to_string(getTotalLanternFishCount( LanternFish(getRawLanternFish("input.txt")), 256)) << endl;
}
