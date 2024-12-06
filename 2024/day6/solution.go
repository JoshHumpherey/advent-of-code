package main

import (
	"advent-of-code/lib"
	"fmt"
	"sync"
)

type Direction int

const (
	Up Direction = iota
	Right
	Down
	Left
	Init
)

type grid struct {
	matrix  [][]string
	visited [][][]Direction
	guard   []int
	dir     Direction
}

func (g *grid) getVisitedCount() int {
	total := 0
	for r := range g.visited {
		for c := range g.visited[0] {
			if len(g.visited[r][c]) > 1 {
				total += 1
			}
		}
	}
	return total
}

func (g *grid) addDir(r, c int, dir Direction) {
	seen := g.visited[r][c]
	for _, s := range seen {
		if s == dir {
			return
		}
	}
	g.visited[r][c] = append(g.visited[r][c], dir)
}

func (g *grid) alreadyVisited(r, c int, dir Direction) bool {
	seen := g.visited[r][c]
	for _, s := range seen {
		if s == dir {
			return true
		}
	}
	return false
}

func getGrid(filePath string) (grid, error) {
	matrix, err := lib.ParseStringMatrix(filePath)
	if err != nil {
		return grid{}, err
	}
	visited := make([][][]Direction, 0)
	guard := []int{}
	for r := range matrix {
		row := [][]Direction{}
		for c := range matrix[0] {
			if matrix[r][c] == "^" {
				guard = []int{r, c}
				matrix[r][c] = "."
				row = append(row, []Direction{Up})
			} else {
				row = append(row, []Direction{Init})
			}
		}
		visited = append(visited, row)
	}

	return grid{
		matrix:  matrix,
		visited: visited,
		guard:   guard,
		dir:     Up,
	}, nil
}

func getNextDir(d Direction) Direction {
	switch d {
	case Up:
		return Right
	case Right:
		return Down
	case Down:
		return Left
	case Left:
		return Up
	default:
		return Up
	}
}

func getNextCoordinatePair(pair []int, d Direction) []int {
	switch d {
	case Up:
		return []int{pair[0] - 1, pair[1]}
	case Right:
		return []int{pair[0], pair[1] + 1}
	case Down:
		return []int{pair[0] + 1, pair[1]}
	case Left:
		return []int{pair[0], pair[1] - 1}
	default:
		return []int{pair[0], pair[1]}
	}
}

func getGuardVisitedCount(g grid) int {
	for {
		nextGuard := getNextCoordinatePair(g.guard, g.dir)
		r, c := nextGuard[0], nextGuard[1]
		if r < 0 || c < 0 || r >= len(g.matrix) || c >= len(g.matrix[0]) {
			break
		} else if g.matrix[r][c] == "#" {
			g.dir = getNextDir(g.dir)
			nextGuard = getNextCoordinatePair(g.guard, g.dir)
			r, c = nextGuard[0], nextGuard[1]
		}

		g.guard = []int{r, c}
		g.addDir(r, c, g.dir)
	}
	return g.getVisitedCount()
}

func hasCycle(filePath string, rr, cc int, res chan bool, wg *sync.WaitGroup) {
	defer wg.Done()
	g, err := getGrid(filePath)
	if err != nil {
		res <- false
		return
	}
	if g.matrix[rr][cc] == "#" {
		res <- false
		return
	}
	g.matrix[rr][cc] = "#"

	for {
		nextGuard := getNextCoordinatePair(g.guard, g.dir)
		r, c := nextGuard[0], nextGuard[1]
		if r < 0 || c < 0 || r >= len(g.matrix) || c >= len(g.matrix[0]) {
			break
		} else if g.matrix[r][c] == "#" {
			g.dir = getNextDir(g.dir)
			nextGuard = getNextCoordinatePair(g.guard, g.dir)
			r, c = nextGuard[0], nextGuard[1]
		}

		if g.alreadyVisited(r, c, g.dir) {
			res <- true
			return
		}
		g.guard = []int{r, c}
		g.addDir(r, c, g.dir)
	}
	res <- false
	return
}

func getTotalCycleCount(filePath string, origGrid grid) int {
	results := make(chan bool, len(origGrid.matrix)*len(origGrid.matrix[0]))
	var wg sync.WaitGroup

	for r := range origGrid.matrix {
		for c := range origGrid.matrix[0] {
			wg.Add(1)
			go hasCycle(filePath, r, c, results, &wg)
		}
	}
	wg.Wait()
	close(results)

	total := 0
	for result := range results {
		if result {
			total++
		}
	}
	return total
}

func main() {
	grid, err := getGrid("input.txt")
	if err != nil {
		panic(err)
	}

	part1 := getGuardVisitedCount(grid)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := getTotalCycleCount("input.txt", grid)
	fmt.Printf("Part 2: %d\n", part2)
}