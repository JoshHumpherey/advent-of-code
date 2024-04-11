#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

struct instructions {
    vector<pair<int,int>> points;
    vector<pair<char,int>> folds;
};

pair<string, string> splitString(const string& s, const char delim) {
    string h1;
    string h2;
    bool seenDelim = false;
    for (char i : s) {
        if (i == delim) {
            seenDelim = true;
        } else if (!seenDelim) {
            h1.push_back(i);
        } else {
            h2.push_back(i);
        }
    }
    return make_tuple(h1, h2);
}

instructions getInstructions(const string& filePath) {
    ifstream inputFile(filePath);
    vector<string> lines;
    if (!inputFile) {
        cerr << "Failed to open input file." << endl;
        return {};
    }
    instructions instructions;
    string line;
    bool parsingFolds = false;
    while (getline(inputFile, line)) {
        if (line.empty()) {
            parsingFolds = true;
        } else if (parsingFolds) {
            auto rawPair = splitString(line, '=');
            char dir = rawPair.first[rawPair.first.size()-1];
            auto mag = stoi(rawPair.second);
            instructions.folds.emplace_back(dir, mag);
        } else {
            auto rawPair = splitString(line, ',');
            auto x = stoi(rawPair.first);
            auto y = stoi(rawPair.second);
            instructions.points.emplace_back(x,y);
        }
    }

    return instructions;
}

vector<vector<string>> buildBoard(vector<pair<int,int>> points) {
    vector<vector<string>> board = {};
    int xMax = 0;
    int yMax = 0;
    for (auto p : points) {
        int x = p.first;
        int y = p.second;
        xMax = max(xMax, x);
        yMax = max(yMax, y);
    }

    for (auto y = 0; y < yMax+1; y++) {
        vector<string> row = {};
        for (auto x = 0; x < xMax+1; x++) {
            row.emplace_back(".");
        }
        board.push_back(row);
    }
    for (auto p : points) {
        int x = p.first;
        int y = p.second;
        board[y][x] = "#";
    }

    return board;
}

void printBoard(vector<vector<string>> board) {
    for (auto y = 0; y < board.size(); y++) {
        string row;
        for (auto x = 0; x < board[0].size(); x++) {
            row += board[y][x];
        }
        cout << row << endl;
    }
    cout << endl;
}

vector<vector<string>> foldOverY(vector<vector<string>> board, int foldPoint) {
    vector<vector<string>> foldedBoard = {};
    for (auto y = 0; y < board.size(); y++) {
        vector<string> newRow = {};
        for (auto x = 0; x < board[0].size(); x++) {
            if (y < foldPoint) {
                newRow.push_back(board[y][x]);
            } else if (y > foldPoint && board[y][x] == "#") {
                int dist = abs(y - foldPoint);
                int mirrorY = foldPoint - dist;
                foldedBoard[mirrorY][x] = "#";
            }
        }
        if (y < foldPoint) {
            foldedBoard.push_back(newRow);
        }
    }
    return foldedBoard;
}

vector<vector<string>> foldOverX(vector<vector<string>> board, int foldPoint) {
    vector<vector<string>> foldedBoard = {};
    for (auto y = 0; y < board.size(); y++) {
        vector<string> newRow = {};
        for (auto x = 0; x < board[0].size(); x++) {
            if (x < foldPoint) {
                newRow.push_back(board[y][x]);
            } else if (x > foldPoint and board[y][x] == "#") {
                int dist = abs(x - foldPoint);
                int mirrorX = foldPoint - dist;
                newRow[mirrorX] = "#";
            }
        }
        foldedBoard.push_back(newRow);
    }
    return foldedBoard;
}

int getTotalDots(vector<vector<string>> board) {
    int total = 0;
    for (auto y = 0; y < board.size(); y++) {
        for (auto x = 0; x < board[0].size(); x++) {
            if (board[y][x] == "#") {
                total += 1;
            }
        }
    }
    return total;
}

void processInstructions(const instructions& instructions) {
    auto board = buildBoard(instructions.points);
    bool firstFold = true;
    int firstFoldCount = 0;

    for (auto f : instructions.folds) {
        auto foldAxis = f.first;
        auto foldMag = f.second;
        if (foldAxis == 'x') {
            board = foldOverX(board, foldMag);
        } else {
            board = foldOverY(board, foldMag);
        }

        if (firstFold) {
            firstFold = false;
            firstFoldCount = getTotalDots(board);
        }
    }
    cout << "First Fold Dots: " + to_string(firstFoldCount) << endl;
    printBoard(board);
}


int main() {
    auto instructions = getInstructions("input.txt");
    processInstructions(instructions);
}