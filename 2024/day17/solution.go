package main

import (
	"advent-of-code/lib"
	"fmt"
	"math"
	"strconv"
	"strings"
	"sync"
	"time"
)

type computer struct {
	a          int
	b          int
	c          int
	program    []int
	pointer    int
	programOut []string
}

func clone(c computer) computer {
	return computer{
		c.a,
		c.b,
		c.c,
		c.program,
		c.pointer,
		c.programOut,
	}
}

func partialMatch(inProgress, target []string) bool {
	if len(inProgress) > len(target) {
		return false
	}
	for i := range inProgress {
		if inProgress[i] != target[i] {
			return false
		}
	}
	return true
}

func getInput(filePath string) (computer, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return computer{}, err
	}
	c := computer{
		pointer: 0,
	}
	program := []int{}
	for i, l := range lines {
		if i >= 0 && i < 3 {
			val, _ := strconv.Atoi(strings.Split(l, ": ")[1])
			if i == 0 {
				c.a = val
			} else if i == 1 {
				c.b = val
			} else {
				c.c = val
			}
		} else if i == 4 {
			programNums := strings.Split(strings.Split(l, ": ")[1], ",")
			for _, n := range programNums {
				val, _ := strconv.Atoi(n)
				program = append(program, val)
			}
			c.program = program
		}
	}
	return c, nil
}

func (c *computer) getCombo(val int) int {
	switch val {
	case 0, 1, 2, 3:
		return val
	case 4:
		return c.a
	case 5:
		return c.b
	case 6:
		return c.c
	default:
		panic(fmt.Errorf("invalid combo value %d", val))
	}
}

func (c *computer) adv(x int) {
	num := c.a
	denom := int(math.Pow(2, float64(x)))
	c.a = num / denom
}

func (c *computer) bxl(x int) {
	c.b = c.b ^ x
}

func (c *computer) bst(x int) {
	c.b = x % 8
}

func (c *computer) jnz(x int) bool {
	if c.a == 0 {
		return false
	}
	c.pointer = x
	return true
}

func (c *computer) bxc() {
	c.b = c.b ^ c.c
}

func (c *computer) out(x int) {
	c.programOut = append(c.programOut, strconv.Itoa(x%8))
}

func (c *computer) bdv(x int) {
	num := c.a
	denom := int(math.Pow(2, float64(x)))
	c.b = num / denom
}

func (c *computer) cdv(x int) {
	num := c.a
	denom := int(math.Pow(2, float64(x)))
	c.c = num / denom
}

func (c *computer) process(opcode, operand int) {
	combo := c.getCombo(operand)
	jumped := false

	switch opcode {
	case 0:
		c.adv(combo)
	case 1:
		c.bxl(operand)
	case 2:
		c.bst(combo)
	case 3:
		jumped = c.jnz(operand)
	case 4:
		c.bxc()
	case 5:
		c.out(combo)
	case 6:
		c.bdv(combo)
	case 7:
		c.cdv(combo)
	}

	if !jumped {
		c.pointer += 2
	}
}

func (c *computer) run() string {
	for c.pointer+1 < len(c.program) {
		opcode := c.program[c.pointer]
		operand := c.program[c.pointer+1]
		c.process(opcode, operand)
	}
	return strings.Join(c.programOut, ",")
}

func findLoopingProgram(orig computer) string {
	programNums := []string{}
	for _, v := range orig.program {
		programNums = append(programNums, strconv.Itoa(v))
	}
	target := strings.Join(programNums, ",")
	res := make(chan (string), 100)
	var wg sync.WaitGroup
	inc := 100_000_000_000

	for a := 0; a <= 500_000_000_000_000; a += inc {
		wg.Add(1)
		go match(target, orig, a, a+inc, res, &wg)
	}

	wg.Wait()
	return <-res
}

func match(target string, orig computer, start, end int, res chan (string), wg *sync.WaitGroup) {
	defer wg.Done()
	for a := start; a <= end; a++ {
		c := clone(orig)
		c.a = a
		output := c.run()
		if output == target {
			fmt.Printf("Found a match! %s\n", output)
			res <- output
			return
		}
	}
	fmt.Printf("Finished range %d to %d\n", start, end)
}

func main() {
	computer, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	c1 := clone(computer)
	part1 := c1.run()
	fmt.Printf("Part 1: %s (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := findLoopingProgram(clone(computer))
	fmt.Printf("Part 2: %s (%s)\n", part2, time.Since(p2Start))
}
