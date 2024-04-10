#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stack>
#include <set>
#include <map>
#include <stdexcept>

using namespace std;

const set<char> opens = {'(', '<', '[', '{'};
const set<char> closes = {')', '>', ']', '}'};
map<char,char> pairs = {{')', '('}, {'>', '<'}, {']', '['}, {'}', '{'}};
map<char,int> closeScoreMap = {{'(', 1}, {'[', 2}, {'{', 3}, {'<', 4}};

struct Chunks {
    vector<string> incomplete;
    vector<string> corrupted;
};

Chunks getChunks(const string& filePath) {
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

    Chunks chunks;
    for (const auto& l : lines) {
        stack<char> stack;
        string toCommit = l;
        bool incomplete = true;

        for (const char& c : l) {
            if (opens.count(c) > 0) {
                stack.push(c);
            } else if (stack.empty()){
                incomplete = true;
                toCommit = l;
                break;
            } else {
                auto val = stack.top();
                stack.pop();
                if (pairs[c] == val) {
                    continue;
                } else {
                    incomplete = false;
                    toCommit = l;
                    break;
                }
            }
        }

        if (incomplete) {
            chunks.incomplete.push_back(toCommit);
        } else {
            chunks.corrupted.push_back(toCommit);
        }

    }
    return chunks;
}

int scoreCorruptedChunks(const vector<string>& corrupted) {
    int total = 0;
    for (const auto& corrupt : corrupted) {
        stack<char> stack;
        for (const char& c : corrupt) {
            if (opens.count(c) > 0) {
                stack.push(c);
            } else {
                auto openChar = stack.top();
                stack.pop();
                if (pairs[c] == openChar) {
                    continue;
                } else if (c == ')') {
                    total += 3;
                } else if (c == ']') {
                    total += 57;
                } else if (c == '}') {
                    total += 1197;
                } else if (c == '>') {
                    total += 25137;
                } else {
                    throw runtime_error("found bad character on matching");
                }
                    break;
                }
            }
        }
    return total;
}

long long scoreIncompleteChunks(const vector<string>& incomplete) {
    vector<long long> scores = {};
    for (const auto& inc : incomplete) {
        stack<char> stack;

        for (const char& c : inc) {
            if (opens.count(c) > 0) {
                stack.push(c);
            } else {
                stack.pop();
            }
        }

        long long total = 0;
        while (!stack.empty()) {
            total *= 5;
            auto toScore = stack.top();
            stack.pop();
            total += closeScoreMap[toScore];
        }
        scores.push_back(total);
    }

    sort(scores.begin(), scores.end());
    return scores[scores.size() / 2];
}


int main() {
    auto chunks = getChunks("input.txt");

    cout << "Part 1: " + to_string(scoreCorruptedChunks(chunks.corrupted)) << endl;
    cout << "Part 2: " + to_string(scoreIncompleteChunks(chunks.incomplete)) << endl;
}