package main

import (
	"advent-of-code/lib"
	"fmt"
	"math"
	"os"
	"os/exec"
	"time"
)

type point struct {
	r int
	c int
}

type Direction int

const (
	Up Direction = iota
	Down
	Right
	Left
)

type Node struct {
	cost int
	r    int
	c    int
	d    Direction
	v    map[int]map[int]map[Direction]int
}

type MinHeap []Node

func (h MinHeap) Len() int {
	return len(h)
}

func (h MinHeap) Less(i, j int) bool {
	return h[i].cost < h[j].cost
}

func (h MinHeap) Swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h *MinHeap) Push(x Node) {
	*h = append(*h, x)
}

func (h *MinHeap) Pop() Node {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func getTurns(d Direction) []Direction {
	switch d {
	case Up:
		return []Direction{Left, Right}
	case Right:
		return []Direction{Up, Down}
	case Down:
		return []Direction{Right, Left}
	case Left:
		return []Direction{Down, Up}
	default:
		return []Direction{}
	}
}

func getNextPair(r, c int, d Direction) (int, int) {
	switch d {
	case Up:
		return r - 1, c
	case Right:
		return r, c + 1
	case Down:
		return r + 1, c
	case Left:
		return r, c - 1
	default:
		return r, c
	}
}

func copy(m map[int]map[int]map[Direction]int) map[int]map[int]map[Direction]int {
	newMap := make(map[int]map[int]map[Direction]int)
	for r, _ := range m {
		for c, _ := range m[r] {
			for d, _ := range m[r][c] {
				if _, ok := newMap[r]; !ok {
					newMap[r] = make(map[int]map[Direction]int)
				}
				if _, ok := newMap[r][c]; !ok {
					newMap[r][c] = make(map[Direction]int)
				}
				newMap[r][c][d] = m[r][c][d]
			}
		}
	}
	return newMap
}

func add(m map[int]map[int]map[Direction]int, r, c int, d Direction, cost int) map[int]map[int]map[Direction]int {
	if _, ok := m[r]; !ok {
		m[r] = make(map[int]map[Direction]int)
	}
	if _, ok := m[r][c]; !ok {
		m[r][c] = make(map[Direction]int)
	}
	m[r][c][d] = cost
	return m
}

func addSeat(m map[int]map[int]bool, r, c int) {
	if _, ok := m[r]; !ok {
		m[r] = make(map[int]bool)
	}
	if _, ok := m[r][c]; !ok {
		m[r][c] = true
	}
}

func print(matrix [][]string, visited map[int]map[int]map[Direction]int) {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()

	for r := range matrix {
		row := ""
		for c := range matrix[0] {
			marked := false
			if _, rExists := visited[r]; rExists {
				if _, cExists := visited[r][c]; cExists {
					marked = true
				}
			}

			if marked {
				row += "O"
			} else {
				row += matrix[r][c]
			}
		}
		fmt.Println(row)
	}
}

func getInput(filePath string) ([][]string, [][]int, point, point, error) {
	matrix, err := lib.ParseStringMatrix(filePath)
	if err != nil {
		return nil, nil, point{}, point{}, err
	}
	costs := make([][]int, 0)
	start := point{}
	end := point{}
	for r := range matrix {
		costRow := []int{}
		for c := range matrix[0] {
			if matrix[r][c] == "S" {
				start = point{r, c}
			} else if matrix[r][c] == "E" {
				end = point{r, c}
			}
			costRow = append(costRow, math.MaxInt)
		}
		costs = append(costs, costRow)
	}

	return matrix, costs, start, end, nil
}

func findMinCostPath(matrix [][]string, costs [][]int, start, end point, dir Direction) int {
	minHeap := MinHeap{}
	minHeap.Push(Node{0, start.r, start.c, dir, make(map[int]map[int]map[Direction]int)})

	for minHeap.Len() > 0 {
		n := minHeap.Pop()
		r, c, d := n.r, n.c, n.d
		if r < 0 || c < 0 || r >= len(matrix) || c >= len(matrix[0]) || matrix[r][c] == "#" {
			continue
		} else if n.cost > costs[r][c] {
			continue
		}

		costs[r][c] = n.cost
		turns := getTurns(d)
		turn1, turn2 := turns[0], turns[1]

		sR, sC := getNextPair(r, c, d)
		t1R, t1C := getNextPair(r, c, turn1)
		t2R, t2C := getNextPair(r, c, turn2)

		minHeap.Push(Node{n.cost + 1, sR, sC, d, n.v})
		minHeap.Push(Node{n.cost + 1001, t1R, t1C, turn1, n.v})
		minHeap.Push(Node{n.cost + 1001, t2R, t2C, turn2, n.v})
	}

	return costs[end.r][end.c]
}

func buildCostMap(matrix [][]string) map[int]map[int]map[Direction]int {
	costs := make(map[int]map[int]map[Direction]int)
	for r := range matrix {
		for c := range matrix[0] {
			if _, ok := costs[r]; !ok {
				costs[r] = make(map[int]map[Direction]int)
			}
			if _, ok := costs[r][c]; !ok {
				costs[r][c] = make(map[Direction]int)
			}
			for _, d := range []Direction{Up, Right, Down, Left} {
				if _, ok := costs[r][c][d]; !ok {
					costs[r][c][d] = math.MaxInt
				}
			}
		}
	}
	return costs
}

func findBestSeats(matrix [][]string, best int, start, end point, dir Direction) int {
	seats := make(map[int]map[int]bool)
	minHeap := MinHeap{}
	minHeap.Push(Node{0, start.r, start.c, dir, make(map[int]map[int]map[Direction]int)})
	costs := buildCostMap(matrix)

	for minHeap.Len() > 0 {
		n := minHeap.Pop()
		r, c, d := n.r, n.c, n.d
		if r < 0 || c < 0 || r >= len(matrix) || c >= len(matrix[0]) || matrix[r][c] == "#" {
			continue
		} else if n.cost > costs[r][c][d] || n.cost > best {
			continue
		} else if end.r == r && end.c == c && n.cost == best {
			n.v = add(n.v, r, c, d, n.cost)
			for rKey := range n.v {
				for cKey := range n.v[rKey] {
					addSeat(seats, rKey, cKey)
				}
			}
		}

		costs[r][c][d] = n.cost
		turns := getTurns(d)
		turn1, turn2 := turns[0], turns[1]

		sR, sC := getNextPair(r, c, d)
		t1R, t1C := getNextPair(r, c, turn1)
		t2R, t2C := getNextPair(r, c, turn2)
		v := add(n.v, r, c, d, n.cost)
		minHeap.Push(Node{n.cost + 1, sR, sC, d, copy(v)})
		minHeap.Push(Node{n.cost + 1001, t1R, t1C, turn1, copy(v)})
		minHeap.Push(Node{n.cost + 1001, t2R, t2C, turn2, copy(v)})
	}

	total := 0
	for r := range seats {
		for range seats[r] {
			total++
		}
	}
	return total
}

func main() {
	matrix, costs, start, end, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := findMinCostPath(matrix, costs, start, end, Right)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := findBestSeats(matrix, costs[end.r][end.c], start, end, Right)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))

}
