#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <utility>


using namespace std;

class Coordinate {
public:
    pair<int, int> start;
    pair<int, int> end;

    Coordinate(int x0, int y0, int x1, int y1) {
        start = make_pair(x0, y0);
        end = make_pair(x1, y1);
    }
};

class Board {
private:
    map<pair<int, int>, int> cells;
public:
    void PlotLine(Coordinate c, bool plotDiagonal) {
        // plot vertical lines if allowed
        if (c.start.first != c.end.first && c.start.second != c.end.second) {
            if (plotDiagonal) {
                pair<int, int> leftPair = c.end;
                pair<int, int> rightPair = c.start;
                if (c.start.second <= c.end.second) {
                    leftPair = c.start;
                    rightPair = c.end;
                }
                int rise = 1;
                if (rightPair.first <= leftPair.first) {
                    rise = -1;
                }

                while (leftPair.first != rightPair.first && leftPair.second != rightPair.second) {
                    auto key = leftPair;
                    if (cells.count(key) > 0) {
                        cells[key] += 1;
                    } else {
                        cells[key] = 1;
                    }

                    leftPair.first += rise;
                    leftPair.second += 1;
                }
                cells[leftPair] += 1;
            }
            return;
        }

        // add all vertical lines
        if (c.start.first != c.end.first) {
            int start_r = min(c.start.first, c.end.first);
            int end_r = max(c.start.first, c.end.first);
            while (start_r <= end_r) {
                auto key = make_pair(start_r, c.start.second);
                if (cells.count(key) > 0) {
                    cells[key] += 1;
                } else {
                    cells[key] = 1;
                }
                start_r += 1;
            }
        }

        // add all horizontal lines
        if (c.start.second != c.end.second) {
            int start_c = min(c.start.second, c.end.second);
            int end_c = max(c.start.second, c.end.second);
            while (start_c <= end_c) {
                auto key = make_pair(c.start.first, start_c);
                if (cells.count(key) > 0) {
                    cells[key] += 1;
                } else {
                    cells[key] = 1;
                }
                start_c += 1;
            }
        }
    }

    int GetIntersectionCount() {
        int intersections = 0;
        for (auto &p : cells) {
            if (p.second >= 2) {
                intersections += 1;
            }
        }
        return intersections;
    }

    void Print() {
        int maxBound = 0;
        for (auto c : cells) {
            int localBound = max(c.first.first, c.first.second);
            maxBound = max(maxBound, localBound);
        }

        for (auto r = 0; r < maxBound + 1; r++) {
            string line = "";
            for (auto c = 0; c < maxBound + 1; c++) {
                auto key = make_pair(r, c);
                if (cells.count(key) > 0) {
                    line += to_string(cells[key]);
                } else {
                    line += ".";
                }
            }
            cout << line << endl;
        }
    }
};

vector<int> extractNumbers(string& s) {
    int fillerSize = 4;
    for (auto i = 0; i < s.size(); i++) {
        if (s[i] == ' ') {
            s.replace(i, fillerSize, ",");
            break;
        }
    }

    vector<int> result = {};
    char delim = ',';

    string temp = "";
    for (auto i = 0; i < s.size(); i++) {
        if (s[i] == delim) {
            result.push_back(stoi(temp));
            temp = "";
        } else {
            temp.push_back(s[i]);
        }
    }
    if (!temp.empty()) {
        result.push_back(stoi(temp));
    }
    return result;
}

vector<Coordinate> parseLines(const string& filePath) {
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

    vector<Coordinate> result = {};
    for (auto & l : lines) {
        auto n = extractNumbers(l);
        result.emplace_back(n[1], n[0], n[3], n[2]);
    }
    return result;
}

int main() {
    vector<Coordinate> coordinates = parseLines("input.txt");
    Board standardBoard;
    Board diagonalBoard;

    for (auto c : coordinates) {
        standardBoard.PlotLine(c, false);
        diagonalBoard.PlotLine(c, true);
    }

    cout << "Part 1: " + to_string(standardBoard.GetIntersectionCount()) << endl;
    cout << "Part 2: " + to_string(diagonalBoard.GetIntersectionCount()) << endl;
}