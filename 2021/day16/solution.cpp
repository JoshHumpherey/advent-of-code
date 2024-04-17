#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cctype>

using namespace std;

const bool DEBUG = false;

const int HEADER_SIZE = 6;
const int LITERAL_ID = 4;
const int NESTED_PACKET_HEADER_SIZE = 7;
const int NESTED_SIZE_LEN = 15;
const int NESTED_COUNT_LEN = 11;

string hexCharToBinary(char hex) {
    hex = toupper(hex);
    switch (hex) {
        case '0': return "0000";
        case '1': return "0001";
        case '2': return "0010";
        case '3': return "0011";
        case '4': return "0100";
        case '5': return "0101";
        case '6': return "0110";
        case '7': return "0111";
        case '8': return "1000";
        case '9': return "1001";
        case 'A': return "1010";
        case 'B': return "1011";
        case 'C': return "1100";
        case 'D': return "1101";
        case 'E': return "1110";
        case 'F': return "1111";
        default: return ""; // Invalid hex character
    }
}

long long binaryStringToLongLong(const string& binaryString) {
    return stol(binaryString, nullptr, 2);
}

string getBinaryInput(const string& filePath) {
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
    string binary;
    for (auto c : lines[0]) {
        binary += hexCharToBinary(c);
    }
    return binary;
}

long long getVectorSum(const vector<long long>& v) {
    long long res = 0;
    for (const auto& val : v) {
        res += val;
    }
    return res;
}

long long getVectorProduct(const vector<long long>& v) {
    long long res = 1;
    for (const auto& val : v) {
        res *= val;
    }
    return res;
}

long long getVectorMin(const vector<long long>& v)  {
    long long res = LLONG_MAX;
    for (const auto& val : v) {
        res = min(res, val);
    }
    return res;
}

long long getVectorMax(const vector<long long>& v)  {
    long long res = LLONG_MIN;
    for (const auto& val : v) {
        res = max(res, val);
    }
    return res;
}

long long getGreaterThan(const vector<long long>& v) {
    if (v[0] > v[1]) {
        return 1ll;
    }
    return 0ll;
}

long long getLessThan(const vector<long long>& v) {
    if (v[0] < v[1]) {
        return 1ll;
    }
    return 0ll;
}

long long getEqualTo(const vector<long long>& v) {
    if (v[0] == v[1]) {
        return 1ll;
    }
    return 0ll;
}


long long parsePacket(const string& binaryString, long long& position, bool returnVersionSum) {
    if (DEBUG)
        cout << binaryString.substr(position, binaryString.size()-position) << endl;

    auto version = binaryStringToLongLong(binaryString.substr(position, 3));
    auto id = binaryStringToLongLong(binaryString.substr(position+3, 3));

    if (DEBUG)
        cout << "version: " + to_string(version) + ", id: " + to_string(id) << endl;
    long long versionSum = version;

    if (id == LITERAL_ID) {
        position += HEADER_SIZE;
        string val;
        while (binaryString[position] == '1') {
            val += binaryString.substr(position+1, 4);
            position += 5;
        }
        val += binaryString.substr(position+1, 4);
        position += 5;
        if (returnVersionSum) {
           return versionSum;
        }
        auto res = binaryStringToLongLong(val);
        if (DEBUG)
            cout << "Literal Value=" + to_string(res) << endl;
        return res;
    } else {
        vector<long long> values = {};
        char operatorId = binaryString[position+HEADER_SIZE];
        if (operatorId == '0') {
            position += NESTED_PACKET_HEADER_SIZE;
            auto nestedSize = binaryStringToLongLong(binaryString.substr(position, NESTED_SIZE_LEN));
            if (DEBUG)
                cout << "parsing sub-packets with size " + to_string(nestedSize) << endl;
            long long length = position + NESTED_SIZE_LEN + nestedSize;
            position += NESTED_SIZE_LEN;
            while(position != length) {
                values.push_back(parsePacket(binaryString, position, returnVersionSum));
            }
        } else {
            long long packetCount = binaryStringToLongLong(binaryString.substr(position + NESTED_PACKET_HEADER_SIZE, NESTED_COUNT_LEN));
            if (DEBUG)
                cout << "parsing " + to_string(packetCount) + " sub-packet(s) from " + binaryString.substr(position + NESTED_PACKET_HEADER_SIZE, NESTED_COUNT_LEN) << endl;
            position += (NESTED_PACKET_HEADER_SIZE + NESTED_COUNT_LEN);
            for(long long i = 0; i < packetCount; i++) {
                values.push_back(parsePacket(binaryString, position, returnVersionSum));
            }
        }

        if (returnVersionSum) {
            return versionSum + getVectorSum(values);
        }
        switch (id) {
            case 0: return getVectorSum(values);
            case 1: return getVectorProduct(values);
            case 2: return getVectorMin(values);
            case 3: return getVectorMax(values);
            case 5: return getGreaterThan(values);
            case 6: return getLessThan(values);
            case 7: return getEqualTo(values);
            default: return -1;
        }
    }
}


int main() {
    string input = getBinaryInput("input.txt");
    long long position = 0;

    // cout << "Part 1: " + to_string(parsePacket(input, position, true)) << endl;
    cout << "Part 2: " + to_string(parsePacket(input, position, false)) << endl;
}