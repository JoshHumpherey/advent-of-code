package main

import (
	"advent-of-code/lib"
	"fmt"
	"strconv"
	"strings"
	"time"
)

type point struct {
	x int
	y int
}

type claw struct {
	a point
	b point
	p point
}

func parsePoint(s, delim string) point {
	rawButton := strings.Split(s, ": ")[1]
	splitButtons := strings.Split(rawButton, ", ")
	x, _ := strconv.Atoi(strings.Split(splitButtons[0], delim)[1])
	y, _ := strconv.Atoi(strings.Split(splitButtons[1], delim)[1])
	return point{
		x: x,
		y: y,
	}
}

func createClaw(group []string) claw {
	a := parsePoint(group[0], "+")
	b := parsePoint(group[1], "+")
	p := parsePoint(group[2], "=")
	return claw{a: a, b: b, p: p}
}

func getInput(filePath string) ([]claw, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return nil, err
	}
	claws := []claw{}
	group := []string{}
	for _, l := range lines {
		if l == "" {
			claws = append(claws, createClaw(group))
			group = []string{}
		} else {
			group = append(group, l)
		}
	}
	if len(group) != 0 {
		claws = append(claws, createClaw(group))
	}
	return claws, nil
}

func calculateTokens(c claw) int {
	aPoints := make(map[point]int)
	aPoints[point{0, 0}] = 0
	bPoints := make(map[point]int)
	bPoints[c.p] = 0

	x, y := 0, 0
	presses := 1
	for x <= c.p.x && y <= c.p.y {
		x += c.a.x
		y += c.a.y
		aPoints[point{x, y}] = presses
		presses++
	}

	x, y = c.p.x, c.p.y
	presses = 1
	for x >= 0 && y >= 0 {
		x -= c.b.x
		y -= c.b.y
		bPoints[point{x, y}] = presses
		presses++
	}

	for targetPoint := range aPoints {
		if _, exists := bPoints[targetPoint]; exists {
			return 3*aPoints[targetPoint] + bPoints[targetPoint]
		}
	}
	return 0
}

func solveTokens(c claw, offset int) int {
	c.p.x += offset
	c.p.y += offset

	aNum := (c.p.x * c.b.y) - (c.b.x * c.p.y)
	aDenom := (c.a.x * c.b.y) - (c.b.x * c.a.y)
	a := aNum / aDenom

	bNum := (c.p.y * c.a.x) - (c.p.x * c.a.y)
	bDenom := (c.b.y * c.a.x) - (c.b.x * c.a.y)
	b := bNum / bDenom

	xFinal := c.a.x*a + c.b.x*b
	yFinal := c.a.y*a + c.b.y*b
	if xFinal == c.p.x && yFinal == c.p.y {
		return 3*a + b
	}
	return 0
}

func calculateTotalTokens(claws []claw) int {
	tokens := 0
	for _, c := range claws {
		tokens += calculateTokens(c)
	}
	return tokens
}

func solveTotalTokens(claws []claw) int {
	tokens := 0
	for _, c := range claws {
		tokens += solveTokens(c, 10_000_000_000_000)
	}
	return tokens
}

func main() {
	claws, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := calculateTotalTokens(claws)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := solveTotalTokens(claws)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
