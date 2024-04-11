#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

bool isUppercase(const std::string& str) {
    for (char c : str) {
        if (!std::isupper(c)) {
            return false;
        }
    }
    return true;
}

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

map<string,vector<string>> buildGraph(const string& filePath) {
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

    map<string,vector<string>> graph;
    for (const auto& l : lines) {
        auto pair = splitString(l, '-');
        graph[pair.first].push_back(pair.second);
        graph[pair.second].push_back(pair.first);
    }

//    for (auto p : graph) {
//        string vals;
//        for (auto v : p.second) {
//            vals += v + ",";
//        }
//        cout << "Key: " + p.first + ", Values: " +  vals << endl;
//    }
    return graph;
}

map<string,int> buildVisited(const map<string,vector<string>> graph) {
    map<string,int> visited;
    for (const auto& p : graph) {
        visited[p.first] = 0;
    }
    return visited;
}

int uniquePaths(map<string,vector<string>> graph, map<string,int> visited, bool canDoubleBack, const string& id) {
    if (id == "end") {
        return 1;
    }
    int total = 0;
    visited[id] += 1;
    for (const string& nextId : graph[id]) {
        if (nextId == "start") {
            continue;
        } else if (isUppercase(nextId) || visited[nextId] == 0) {
            total += uniquePaths(graph, visited, canDoubleBack, nextId);
        } else if (visited[nextId] == 1 && canDoubleBack) {
            total += uniquePaths(graph, visited, false, nextId);
        }
    }
    return total;
}

int main() {
    auto graph = buildGraph("input.txt");
    auto visited = buildVisited(graph);

    cout << "Part 1: " + to_string(uniquePaths(graph, visited, false, "start")) << endl;
    cout << "Part 2: " + to_string(uniquePaths(graph, visited, true, "start")) << endl;
}