package main

import (
    "fmt"
    "io/ioutil"
	"time"
	"strings"
)

type group struct {
	answers []string
	counts map[string]int
} 

func createAlphaMap(answers []string) map[string]int {
	m := make(map[string]int)
	for i := 'a'; i <= 'z'; i++ {
		m[string(i)] = 0
	}
	
	// populate the map
	for _, answer := range answers {
		for _, char := range answer {
			m[string(char)] += 1
		}
	}
	return m
}

func createGroups(data []string) []group {
	var groups []group
	var answers []string
	for i, l := range data {
		if l == "" || i == len(data) - 1 {
			if i == len(data)-1 {
				answers = append(answers, l)
			}
			g := group{
				answers: answers,
				counts: createAlphaMap(answers),
			}
			groups = append(groups, g)
			answers = []string{}
		} else {
			answers = append(answers, l)
		}
	}
	return groups
}

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	return strings.Split(string(content), "\n"), nil
}

func main() {
	start := time.Now()

	rawInput, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	}

	groups := createGroups(rawInput)
	sums := 0
	for _, g := range groups {
		localSum := 0
		for _, v := range g.counts {
			if v == len(g.answers) {
				localSum += 1
			}
		}
		sums += localSum
	}
	
	fmt.Println(sums)

	duration := time.Since(start)
	fmt.Println(duration)
}