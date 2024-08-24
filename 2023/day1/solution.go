package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"unicode"
)

var NUMS = []string{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
var VALS = map[string]int{
	"one":   1,
	"two":   2,
	"three": 3,
	"four":  4,
	"five":  5,
	"six":   6,
	"seven": 7,
	"eight": 8,
	"nine":  9,
}

func getInput(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	lines := make([]string, 0)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, nil
}

func getNumber(line string) int {
	nums := []string{}
	for i := 0; i < len(line); i++ {
		char := line[i]
		if unicode.IsDigit(rune(char)) {
			nums = append(nums, string(char))
		}
	}
	toConvert := nums[0] + nums[len(nums)-1]
	val, _ := strconv.Atoi(toConvert)
	return val
}

func getCalibrationSum(lines []string) int {
	sum := 0
	for _, l := range lines {
		sum += getNumber(l)
	}
	return sum
}

func getLeft(line string) (int, error) {
	for i := 0; i < len(line); i++ {
		if unicode.IsDigit(rune(line[i])) {
			val, _ := strconv.Atoi(string(line[i]))
			return val, nil
		}
		for _, toMatch := range NUMS {
			if i+len(toMatch) > len(line) {
				continue
			} else if line[i:i+len(toMatch)] == toMatch {
				return VALS[toMatch], nil
			}
		}
	}

	return -1, fmt.Errorf("unable to find a value (left): %s", line)
}

func getRight(line string) (int, error) {
	for i := len(line) - 1; i >= 0; i-- {
		if unicode.IsDigit(rune(line[i])) {
			val, _ := strconv.Atoi(string(line[i]))
			return val, nil
		}
		for _, toMatch := range NUMS {
			if i+len(toMatch) > len(line) {
				continue
			} else if line[i:i+len(toMatch)] == toMatch {
				return VALS[toMatch], nil
			}
		}
	}

	return -1, fmt.Errorf("unable to find a value (right): %s", line)
}

func getModifiedCalibrationSum(lines []string) (int, error) {
	sum := 0
	for _, l := range lines {
		left, err := getLeft(l)
		if err != nil {
			return 0, err
		}
		right, err := getRight(l)
		if err != nil {
			return 0, err
		}
		combined := strconv.Itoa(left) + strconv.Itoa(right)
		val, _ := strconv.Atoi(combined)
		sum += val
	}
	return sum, nil
}

func main() {
	lines, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	part1 := getCalibrationSum(lines)
	fmt.Printf("Part 1: %d\n", part1)

	part2, err := getModifiedCalibrationSum(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2: %d\n", part2)
}
