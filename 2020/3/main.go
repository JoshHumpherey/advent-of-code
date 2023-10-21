package main

import (
    "fmt"
    "io/ioutil"
	"time"
	"strings"
)

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	return strings.Split(string(content), "\n"), nil
}

func simPath(topography []string, x, y int) int {
	r :=0
	c := 0
	bottom := len(topography)-1
	mod := len(topography[0])
	treeCount := 0

	for r <= bottom {
		// fmt.Println(r, c, string(topography[r][c % mod]))
		if string(topography[r][c % mod]) == "#" {
			treeCount += 1
		}
		r += y
		c += x
	}
	return treeCount
}

func main() {
	start := time.Now()
	topography, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	}
	
	a := simPath(topography, 1, 1)
	b := simPath(topography, 3, 1)
	c := simPath(topography, 5, 1)
	d := simPath(topography, 7, 1)
	e := simPath(topography, 1, 2)
	fmt.Println(a * b * c * d * e)

	duration := time.Since(start)
	fmt.Println(duration)
}