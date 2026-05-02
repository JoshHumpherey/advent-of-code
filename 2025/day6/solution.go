package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func getInput() [][]string {
	data, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}

	output := [][]string{}
	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		output = append(output, strings.Fields(line))
	}
	return output
}

func getColumnValue(worksheet [][]string, column int) int {
	operator := worksheet[len(worksheet)-1][column]
	value, _ := strconv.Atoi(worksheet[0][column])

	for i := 1; i < len(worksheet)-1; i++ {
		val, _ := strconv.Atoi(worksheet[i][column])
		if operator == "+" {
			value += val
		} else if operator == "*" {
			value *= val
		} else if operator == "-" {
			value -= val
		} else if operator == "/" {
			value /= val
		}
	}
	return value
}

func convertToCephalopodNumbers(numbers []string) []int {
	maxLen := 0
	for _, n := range numbers {
		if len(n) > maxLen {
			maxLen = len(n)
		}
	}

	paddedNumbers := []string{}
	for _, n := range numbers {
		paddedNumbers = append(paddedNumbers, strings.Repeat(" ", maxLen-len(n))+n)
	}
	fmt.Println(paddedNumbers)

	rawCephalopodNumbers := []string{}
	for c := 0; c < maxLen; c++ {
		col := ""
		for r := 0; r < len(paddedNumbers); r++ {
			if paddedNumbers[r][c] != ' ' {
				col += string(paddedNumbers[r][c])
			}
		}
		rawCephalopodNumbers = append(rawCephalopodNumbers, col)
	}
	fmt.Println(rawCephalopodNumbers)

	cephalopodNumbers := []int{}
	for _, n := range rawCephalopodNumbers {
		n = strings.TrimSpace(n)
		val, _ := strconv.Atoi(n)
		cephalopodNumbers = append(cephalopodNumbers, val)
	}
	return cephalopodNumbers
}

func getLeftToRightColumnValue(worksheet [][]string, column int) int {
	operator := worksheet[len(worksheet)-1][column]
	rawNumbers := []string{}
	for i := 0; i < len(worksheet)-1; i++ {
		rawNumbers = append(rawNumbers, worksheet[i][column])
	}
	cephalopodNumbers := convertToCephalopodNumbers(rawNumbers)
	value := cephalopodNumbers[0]
	for i := 1; i < len(cephalopodNumbers); i++ {
		if operator == "+" {
			value += cephalopodNumbers[i]
		} else if operator == "*" {
			value *= cephalopodNumbers[i]
		} else if operator == "-" {
			value -= cephalopodNumbers[i]
		} else if operator == "/" {
			value /= cephalopodNumbers[i]
		}
	}
	return value
}

func validateWorksheet(worksheet [][]string) int {
	total := 0
	for i := 0; i < len(worksheet[0]); i++ {
		total += getColumnValue(worksheet, i)
	}
	return total
}

func cephalopodWorksheet(worksheet [][]string) int {
	total := 0
	for i := 0; i < len(worksheet[0]); i++ {
		total += getLeftToRightColumnValue(worksheet, i)
	}
	return total
}

func main() {
	lines := getInput()
	part1 := validateWorksheet(lines)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := cephalopodWorksheet(lines)
	fmt.Printf("Part 2: %d\n", part2)
}
