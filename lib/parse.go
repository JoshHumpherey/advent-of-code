package lib

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

func ParseStrings(filePath string) ([]string, error) {
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

func ParseInts(filePath string) ([][]int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	lines := make([][]int, 0)
	for scanner.Scan() {
		arr := []int{}
		l := strings.Split(scanner.Text(), " ")
		for _, v := range l {
			val, _ := strconv.Atoi(v)
			arr = append(arr, val)
		}
		lines = append(lines, arr)
	}
	return lines, nil
}

func ParseStringMatrix(filePath string) ([][]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	grid := make([][]string, 0)
	for scanner.Scan() {
		row := make([]string, 0)
		for _, val := range scanner.Text() {
			row = append(row, string(val))
		}
		grid = append(grid, row)
	}
	return grid, nil
}

func ParseIntegerMatrix(filePath string) ([][]int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	grid := make([][]int, 0)
	for scanner.Scan() {
		row := make([]int, 0)
		for _, val := range scanner.Text() {
			i, _ := strconv.Atoi(string(val))
			row = append(row, i)
		}
		grid = append(grid, row)
	}
	return grid, nil
}
