#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


vector<int> parseDepths(const std::string& filePath) {
    ifstream inputFile(filePath);
    vector<int> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return lines;
    }
    std::string line;
    while (std::getline(inputFile, line)) {
        lines.push_back(stoll(line));
    }
    inputFile.close();
    return lines;
}

int getIncreaseCount(vector<int> depths) {
    int increases = 0;
    for (int i = 1; i < depths.size(); i++) {
        if (depths[i] > depths[i-1]) {
            increases++;
        }
    }
    return increases;
}

int getSlidingWindowIncreaseCount(vector<int> depths) {
    int increases = 0;
    for (int i = 0; i < depths.size(); i++) {
        if (i < 3) {
            continue;
        }
        int prevWindow = depths[i-3] + depths[i-2] + depths[i-1];
        int currWindow = depths[i-2] + depths[i-1] + depths[i];
        if (currWindow > prevWindow) {
            increases++;
        }
    }
    return increases;
}

int main() {
    string filePath = "input.txt";
    vector<int> depths = parseDepths(filePath);

    cout << "Part 1: " + std::to_string(getIncreaseCount(depths)) << endl;
    cout << "Part 2: " + std::to_string(getSlidingWindowIncreaseCount(depths)) << endl;

    return 0;    
}