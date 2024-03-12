#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

class Board {
private:
    vector<vector<bool>> called;
    vector<vector<int>> nums;
    
public:
    Board(const vector<vector<int>> nums) : nums(nums) {
        called = vector<vector<bool>>(5, vector<bool>(5, false));
    }

    void print() {
        cout << "*****************" << endl;
        for (auto r = 0; r < nums.size(); r++) {
            string row = "";
            for (auto c = 0; c < nums[r].size(); c++) {
                if (c != 0) {
                    row.append(",");
                }
                row.append(to_string(nums[r][c]));
            }
            cout << row << endl;
        }
        cout << "*****************" << endl;
    }
};

vector<int> parseBingoNumbers(string numbers) {
    vector<int> bingoNumbers = {};
    stringstream ss(numbers);
    string item;
    while (getline(ss, item, ',')) {
        bingoNumbers.push_back(stoi(item));
    }
    return bingoNumbers;
}

vector<vector<int>> parseBoardNumbers(vector<string> rawBoard) {
    vector<vector<int>> result = {};
    for (auto i = 0; i < rawBoard.size(); i++) {
        vector<int> row = {};
        stringstream ss(rawBoard[i]);
        string item;
        while (ss >> item) {
            row.push_back(stoi(item));
        }
        result.push_back(row);
    }
    return result;
}

vector<int> parseInput(const string& filePath) {
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

    vector<int> bingoNumbers = parseBingoNumbers(lines[0]);
    
    vector<Board> boards = {};
    vector<string> local = {};
    for (auto i = 2; i < lines.size(); i++) {
        if (lines[i] == "") {
            Board b = Board(parseBoardNumbers(local));
            b.print();
            boards.push_back(b);
            local = {};
        } else {
            local.push_back(lines[i]);
        }
    }

    return bingoNumbers;
}

int main() {
    vector<int> numbers = parseInput("input.txt");

    // cout << "Part 1: " + to_string(calculatePowerConsumption(numbers)) << endl;
    // cout << "Part 2: " + to_string(calculateLifeSupportRating(numbers)) << endl;
}