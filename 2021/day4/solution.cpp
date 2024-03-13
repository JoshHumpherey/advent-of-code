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
    bool won;
    
public:
    Board(const vector<vector<int>> nums) : nums(nums) {
        called = vector<vector<bool>>(5, vector<bool>(5, false));
    }

    void mark(const int number) {
        for (auto r = 0; r < nums.size(); r++) {
            for (auto c = 0; c < nums[r].size(); c++) {
                if (nums[r][c] == number) {
                    called[r][c] = true;
                    return;
                }
            }
        }
    }

    bool wins() {
        // check rows for match
        for (auto r = 0; r < nums.size(); r++) {
            bool match = true;
            for (auto c = 0; c < nums[r].size(); c++) {
                if (called[r][c] == false) {
                    match = false;
                    break;
                }
            }
            if (match) {
                won = true;
                return true;
            }
        }

        // check cols for match
        for (auto c = 0; c < nums[0].size(); c++) {
            bool match = true;
            for (auto r = 0; r < nums.size(); r++) {
                if (called[r][c] == false) {
                    match = false;
                    break;
                }
            }
            if (match) {
                won = true;
                return true;
            }
        }

        // check diagonals
        bool forward = called[0][0] && called[1][1] && called[2][2] && called[3][3] && called[4][4];
        bool backward = called[4][0] && called[3][1] && called[2][2] && called[1][3] && called[0][4];
        if (forward || backward) {
            won = true;
            return true;
        }
        return false;
    }

    int score(const int lastCalled) {
        int unmarkedSum = 0;
        for (auto r = 0; r < nums.size(); r++) {
            for (auto c = 0; c < nums[0].size(); c++) {
                if (!called[r][c]) {
                    unmarkedSum += nums[r][c];
                }
            }
        }
        return unmarkedSum * lastCalled;
    }

    bool has_won() {
        return won;
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

tuple<vector<int>, vector<Board>> parseInput(const string& filePath) {
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
            boards.push_back(Board(parseBoardNumbers(local)));
            local = {};
        } else {
            local.push_back(lines[i]);
        }
    }

    return make_tuple(bingoNumbers, boards);
}

vector<int> scoreBoards(vector<int>& numbers, vector<Board> boards) {
    vector<int> scores = {};
    for (auto i = 0; i < numbers.size(); i++) {
        for (auto j = 0; j < boards.size(); j++) {
            if (boards[j].has_won() == false) {
                boards[j].mark(numbers[i]);
                if (boards[j].wins()) {
                    int localScore = boards[j].score(numbers[i]);
                    scores.push_back(localScore);
                }
            }
        }
    }
    return scores;
}



int main() {
    auto [numbers, boards] = parseInput("input.txt");
    vector<int> scores = scoreBoards(numbers, boards);

    cout << "Part 1: " + to_string(scores[0]) << endl;
    cout << "Part 2: " + to_string(scores[scores.size()-1]) << endl;
}