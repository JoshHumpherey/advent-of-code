package main

import (
	"advent-of-code/lib"
	"container/list"
	"fmt"
	"strconv"
	"strings"
	"time"
)

type point struct {
	r int
	c int
}

func getInput(filePath string, size int) ([][]string, []point, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return nil, []point{}, err
	}

	matrix := make([][]string, 0)
	for r := 0; r <= size; r++ {
		row := []string{}
		for c := 0; c <= size; c++ {
			row = append(row, ".")
		}
		matrix = append(matrix, row)
	}

	points := []point{}
	for _, l := range lines {
		data := strings.Split(l, ",")
		r, _ := strconv.Atoi(data[1])
		c, _ := strconv.Atoi(data[0])
		points = append(points, point{r, c})
	}
	return matrix, points, nil
}

func clone(m [][]string) [][]string {
	n := make([][]string, 0)
	for r := range m {
		row := []string{}
		for c := range m[0] {
			row = append(row, m[r][c])
		}
		n = append(n, row)
	}
	return n
}

func drop(matrix [][]string, points []point, amt int) [][]string {
	for i := 0; i < amt; i++ {
		p := points[i]
		matrix[p.r][p.c] = "#"
	}
	return matrix
}

func bfs(matrix [][]string, size int) int {
	queue := list.New()
	nextQueue := list.New()
	queue.PushBack(point{0, 0})
	cost := 0

	for queue.Len() > 0 {
		for queue.Len() > 0 {
			front := queue.Front()
			queue.Remove(front)
			p := front.Value.(point)

			if p.r < 0 || p.c < 0 || p.r > size || p.c > size || matrix[p.r][p.c] == "#" {
				continue
			} else if p.r == size && p.c == size {
				return cost
			}
			matrix[p.r][p.c] = "#"
			dirs := [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
			for _, d := range dirs {
				rr, cc := p.r+d[0], p.c+d[1]
				nextQueue.PushBack(point{rr, cc})
			}
		}
		queue = nextQueue
		nextQueue = list.New()
		cost++
	}
	return -1
}

func getFirstBlocked(matrix [][]string, points []point, size int) string {
	for _, p := range points {
		matrix[p.r][p.c] = "#"
		if bfs(clone(matrix), size) == -1 {
			s1, s2 := strconv.Itoa(p.c), strconv.Itoa(p.r)
			return strings.Join([]string{s1, s2}, ",")
		}
	}
	return ""
}

func main() {
	size := 70

	matrix, points, err := getInput("input.txt", size)
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	p1Matrix := clone(matrix)
	drop(p1Matrix, points, 1024)
	part1 := bfs(p1Matrix, size)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := getFirstBlocked(clone(matrix), points, size)
	fmt.Printf("Part 2: %s (%s)\n", part2, time.Since(p2Start))
}
