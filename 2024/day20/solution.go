package main

import (
	"advent-of-code/lib"
	"container/list"
	"fmt"
	"math"
	"time"
)

type point struct {
	r int
	c int
}

type jumpPoint struct {
	r    int
	c    int
	size int
}

type grid struct {
	matrix [][]string
	costs  [][]int
	start  point
	end    point
}

func buildCosts(matrix [][]string, start, end point) [][]int {
	costs := make([][]int, 0)
	for range matrix {
		row := []int{}
		for range matrix[0] {
			row = append(row, math.MaxInt)
		}
		costs = append(costs, row)
	}

	next := []point{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	visited := make(map[point]bool)
	queue := list.New()
	nextQueue := list.New()
	cost := 0
	queue.PushBack(start)

	for queue.Len() > 0 {
		for queue.Len() > 0 {
			front := queue.Front()
			queue.Remove(front)
			p := front.Value.(point)

			if _, seen := visited[p]; seen {
				continue
			} else if p.r < 0 || p.c < 0 || p.r >= len(matrix) || p.c >= len(matrix) || matrix[p.r][p.c] == "#" {
				continue
			} else if p.r == end.r && p.c == end.c {
				costs[p.r][p.c] = cost
				return costs
			}

			costs[p.r][p.c] = cost
			visited[p] = true
			for _, n := range next {
				r, c := p.r+n.r, p.c+n.c
				nextQueue.PushBack(point{r, c})
			}
		}
		cost++
		queue = nextQueue
		nextQueue = list.New()
	}
	return costs
}

func getInput(filePath string) (grid, error) {
	matrix, err := lib.ParseStringMatrix(filePath)
	if err != nil {
		return grid{}, err
	}

	g := grid{matrix: matrix}
	for r := range matrix {
		for c := range matrix[0] {
			if matrix[r][c] == "S" {
				g.start = point{r, c}
			} else if matrix[r][c] == "E" {
				g.end = point{r, c}
			}
		}
	}
	g.costs = buildCosts(matrix, g.start, g.end)
	return g, nil
}

func add(m map[point]map[point]bool, start, end point) map[point]map[point]bool {
	if _, ok := m[start]; !ok {
		m[start] = make(map[point]bool)
	}
	if _, ok := m[start][end]; !ok {
		m[start][end] = true
	}
	m[start][end] = true
	return m
}

func exists(m map[point]map[point]bool, start, end point) bool {
	if _, ok := m[start]; !ok {
		return false
	}
	if _, ok := m[start][end]; !ok {
		return false
	}
	return true
}

func walk(matrix [][]string, costs [][]int, start point, distance int) []jumpPoint {
	visited := make(map[point]bool)
	queue := list.New()
	nextQueue := list.New()
	queue.PushBack(start)
	next := []point{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	curr := 0
	res := []jumpPoint{}

	for queue.Len() > 0 && curr <= distance {
		for queue.Len() > 0 {
			front := queue.Front()
			queue.Remove(front)
			p := front.Value.(point)

			if p.r >= 0 && p.c >= 0 && p.r < len(matrix) && p.c < len(matrix[0]) && costs[p.r][p.c] != math.MaxInt && matrix[p.r][p.c] != "#" {
				res = append(res, jumpPoint{p.r, p.c, curr})
			}

			if _, seen := visited[p]; seen {
				continue
			} else if p.r < 0 || p.c < 0 || p.r >= len(matrix) || p.c >= len(matrix[0]) {
				continue
			}

			visited[p] = true
			for _, n := range next {
				r, c := p.r+n.r, p.c+n.c
				np := point{r, c}
				if _, seen := visited[np]; !seen {
					nextQueue.PushBack(np)
				}
			}
		}
		curr++
		queue = nextQueue
		nextQueue = list.New()
	}

	return res
}

func getCheatsOverThreshold(g grid, threshold, jump int) int {
	next := []point{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	visited := make(map[point]bool)
	queue := list.New()
	nextQueue := list.New()
	queue.PushBack(g.start)
	cheatCount := 0
	cheatMap := make(map[point]map[point]bool)

	for queue.Len() > 0 {
		for queue.Len() > 0 {
			front := queue.Front()
			queue.Remove(front)
			p := front.Value.(point)
			if _, exists := visited[p]; exists {
				continue
			} else if p.r < 0 || p.c < 0 || p.r >= len(g.matrix) || p.c >= len(g.matrix) || g.matrix[p.r][p.c] == "#" || g.costs[p.r][p.c] == math.MaxInt {
				continue
			}
			visited[p] = true
			jumps := walk(g.matrix, g.costs, p, jump)
			for _, jp := range jumps {
				diff := g.costs[jp.r][jp.c] - g.costs[p.r][p.c] - jp.size
				normalizedPoint := point{jp.r, jp.c}
				if diff >= threshold && !exists(cheatMap, p, normalizedPoint) {
					cheatMap = add(cheatMap, p, normalizedPoint)
					cheatCount++
				}
			}

			for _, n := range next {
				r, c := p.r+n.r, p.c+n.c
				nextQueue.PushBack(point{r, c})
			}
		}
		queue = nextQueue
		nextQueue = list.New()
	}
	return cheatCount
}

func main() {
	grid, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := getCheatsOverThreshold(grid, 100, 2)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := getCheatsOverThreshold(grid, 100, 20)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
