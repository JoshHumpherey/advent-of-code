package main

import (
    "fmt"
    "io/ioutil"
	"time"
	"strings"
	"sort"
)

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	return strings.Split(string(content), "\n"), nil
}

type boardingPass struct {
	row int
	seat int
	id int
}

func binarySearch(low, high int, data string) int {
	// fmt.Printf("Bounds: %d - %d\n", low, high)
	curr := string(data[0])
	// handle case where we have to choose between the two remaining seats
	if len(data) == 1 {
		if curr == "F" || curr == "L" {
			return low
		} else {
			return high
		}
	}
	midpoint := high - ((high - low) / 2)
	rem := string(data[1:])
	if curr == "F" || curr == "L" {
		return binarySearch(low, midpoint-1, rem)
	} else {
		return binarySearch(midpoint, high, rem)
	}
}

func parseBoardingPass(data string) boardingPass {
	row := binarySearch(0, 127, string(data[0:7]))
	seat := binarySearch(0, 7, string(data[7:]))
	return boardingPass{
		row: row,
		seat: seat,
		id: row * 8 + seat,
	}
}

func main() {
	start := time.Now()

	rawInput, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	} 
	
	var seatIds []int
	for _, data := range rawInput {
		p := parseBoardingPass(data)
		seatIds = append(seatIds, p.id)
	}

	sort.Ints(seatIds)
	
	for i := 1; i < len(seatIds)-1; i++ {
		if seatIds[i-1] != seatIds[i] - 1 {
			fmt.Println(seatIds[i]-1)
			break
		} else if seatIds[i+1] != seatIds[i]+1 {
			fmt.Println(seatIds[i]+1)
			break
		}
	}

	duration := time.Since(start)
	fmt.Println(duration)
}