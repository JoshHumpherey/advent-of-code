package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Game struct {
	ID     int
	Rounds []map[string]int
}

func getInput(filePath string) ([]Game, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return []Game{}, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	res := []Game{}

	for scanner.Scan() {
		line := scanner.Text()
		data := strings.Split(line, ": ")

		id, _ := strconv.Atoi(strings.Split(data[0], " ")[1])
		rounds := strings.Split(data[1], "; ")
		g := Game{ID: id}

		for _, r := range rounds {
			cubes := strings.Split(r, ", ")
			nextRound := map[string]int{}
			for _, c := range cubes {
				colorData := strings.Split(c, " ")
				amt, _ := strconv.Atoi(colorData[0])
				color := colorData[1]
				nextRound[color] = amt
			}
			g.Rounds = append(g.Rounds, nextRound)
		}
		res = append(res, g)
	}
	return res, nil
}

func getValidRounds(games []Game) int {
	sum := 0
	for _, g := range games {
		possible := true
		for _, r := range g.Rounds {
			STANDARD := map[string]int{
				"red":   12,
				"green": 13,
				"blue":  14,
			}
			for color, amt := range r {
				STANDARD[color] -= amt
				if STANDARD[color] < 0 {
					possible = false
				}
			}
		}
		if possible {
			sum += g.ID
		}
	}
	return sum
}

func getMinimumCounts(games []Game) int {
	powers := 0
	for _, g := range games {
		MINIMUM := map[string]int{
			"red":   0,
			"green": 0,
			"blue":  0,
		}
		for _, r := range g.Rounds {
			for color, amt := range r {
				MINIMUM[color] = max(MINIMUM[color], amt)
			}
		}
		powers += MINIMUM["red"] * MINIMUM["green"] * MINIMUM["blue"]
	}
	return powers
}

func main() {
	games, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}
	part1 := getValidRounds(games)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := getMinimumCounts(games)
	fmt.Printf("Part 2: %d\n", part2)
}
