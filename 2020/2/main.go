package main

import (
    "fmt"
    "io/ioutil"
	"strings"
	"strconv"
	"time"
)

type password struct {
	target string
	lowBound int
	highBound int
	input string
}

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	return strings.Split(string(content), "\n"), nil
}

func buildPasswords(rawInput []string) []password {
	var passwords []password
	for _, input := range rawInput {
		chunks := strings.Split(input, " ")
		bounds := strings.Split(chunks[0], "-")
		low, _ := strconv.Atoi(bounds[0])
		high, _ := strconv.Atoi(bounds[1])
		target := strings.TrimSuffix(chunks[1], ":")
		p := password{
			target: target,
			lowBound: low,
			highBound: high,
			input: chunks[2],
		}
		passwords = append(passwords, p)
	}
	return passwords
}

func isValid(pw password) bool {
	sawValidChar := false
	for i, char := range pw.input {
		if string(char) == pw.target && (i+1 == pw.lowBound || i+1 == pw.highBound) {
			if sawValidChar == false {
				sawValidChar = true
			} else {
				// saw the character twice
				return false
			}
		}
	}
	return sawValidChar
} 

func main() {
	start := time.Now()
	rawInput, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	}
	
	pw := buildPasswords(rawInput)
	valid := 0
	for _, p := range pw {
		if isValid(p) {
			valid += 1
		}
	}
	fmt.Println(valid)

	duration := time.Since(start)
	fmt.Println(duration)
}