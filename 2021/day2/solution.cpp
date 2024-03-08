#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <tuple>

using namespace std;

tuple<string, string> splitString(const string s, const char delim) {
    string h1 = "";
    string h2 = "";
    bool seenDelim = false;

    for (int i = 0; i < s.size(); i++) {
        if (s[i] == delim) {
            seenDelim = true;
        } else if (!seenDelim) {
            h1.push_back(s[i]);
        } else {
            h2.push_back(s[i]);
        }
    }
    return make_tuple(h1, h2);
}

vector<string> parseInstructions(const string filePath) {
    ifstream inputFile(filePath);
    vector<string> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return lines;
    }
    string line;
    while (std::getline(inputFile, line)) {
        lines.push_back(line);
    }
    inputFile.close();
    return lines;
}

int getSimplePosition(vector<string> instructions) {
    int depth = 0;
    int horizontal = 0;

    for (const string& ins : instructions) {
        auto [dir, mag] = splitString(ins, ' ');
        if (dir == "forward") {
            horizontal += stoll(mag);
        } else if (dir == "down") {
            depth += stoll(mag);
        } else {
            depth -= stoll(mag);
        }
    }
    return depth * horizontal;
}

int getComplexPosition(vector<string> instructions) {
    int depth = 0;
    int horizontal = 0;
    int aim = 0;

    for (const string& ins : instructions) {
        auto [dir, mag] = splitString(ins, ' ');
        if (dir == "forward") {
            horizontal += stoll(mag);
            depth += (aim * stoll(mag));
        } else if (dir == "down") {
            aim += stoll(mag);
        } else {
            aim -= stoll(mag);
        }
    }
    return depth * horizontal;
}


int main() {;
    vector<string> instructions = parseInstructions("input.txt");

    cout << "Part 1: " + to_string(getSimplePosition(instructions)) << endl;
    cout << "Part 2: " + to_string(getComplexPosition(instructions)) << endl;

    return 0;    
}