#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 2 ]; then
  echo "Please provide the year and day as arguments."
  exit 1
fi

year=$1
day=$2

# Create the year directory if it doesn't exist
if [ ! -d "$year" ]; then
  mkdir "$year"
fi

# Create the day directory if it doesn't exist
if [ ! -d "$year/day$day" ]; then
  mkdir "$year/day$day"
fi

# Create the solution.go file if it doesn't exist and add the specified code
if [ ! -f "$year/day$day/solution.go" ]; then
  echo "package main

import (
	\"bufio\"
	\"fmt\"
	\"os\"
)

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

func dummy(lines []string) int {
	return 0
}

func main() {
	lines, err := getInput(\"input.txt\")
	if err != nil {
		panic(err)
	}

	part1 := dummy(lines)
	fmt.Printf(\"Part 1: %d\n\", part1)
}" > "$year/day$day/solution.go"
fi

# Create the input.txt file if it doesn't exist
if [ ! -f "$year/day$day/input.txt" ]; then
  touch "$year/day$day/input.txt"
fi