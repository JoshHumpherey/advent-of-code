package main

import (
	"advent-of-code/lib"
	"fmt"
	"math"
	"strconv"
	"strings"
)

func getInput(fileName string) ([][]int, error) {
	lines, err := lib.ParseStrings(fileName)
	if err != nil {
		return nil, err
	}

	reports := make([][]int, 0)
	for _, l := range lines {
		report := []int{}
		rawNums := strings.Split(l, " ")
		for _, n := range rawNums {
			num, _ := strconv.Atoi(n)
			report = append(report, num)
		}
		reports = append(reports, report)
	}
	return reports, nil
}

func isSafe(reports []int) bool {
	ascending := true
	for i := range reports {
		if i == 0 {
			continue
		} else if i == 1 {
			if reports[i] < reports[i-1] {
				ascending = false
			}
		}

		if reports[i] < reports[i-1] && ascending {
			return false
		} else if reports[i] > reports[i-1] && !ascending {
			return false
		}

		diff := math.Abs(float64(reports[i]) - float64(reports[i-1]))
		if diff < 1 || diff > 3 {
			return false
		}
	}
	return true
}

func getSafeReports(reports [][]int) int {
	count := 0
	for _, r := range reports {
		if isSafe(r) {
			count += 1
		}
	}
	return count
}

func getSkippedReport(report []int, idx int) []int {
	skippedReport := []int{}
	for i := range report {
		if i != idx {
			skippedReport = append(skippedReport, report[i])
		}
	}
	return skippedReport
}

func getSafeSkippedReports(reports [][]int) int {
	count := 0
	for _, r := range reports {
		for i := range r {
			if isSafe(getSkippedReport(r, i)) {
				count += 1
				break
			}
		}
	}
	return count
}

func main() {
	reports, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	part1 := getSafeReports(reports)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := getSafeSkippedReports(reports)
	fmt.Printf("Part 2: %d\n", part2)
}
