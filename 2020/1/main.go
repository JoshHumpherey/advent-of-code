package main

import (
    "fmt"
    "io/ioutil"
	"strings"
	"strconv"
	"time"
)

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	return strings.Split(string(content), "\n"), nil
}

func convertInputToNums(strNums []string) []int {
	var nums []int
	for _, n := range strNums {
		i, _ := strconv.Atoi(n)
		nums = append(nums, i)
	}
	return nums
}

func createNumMap(nums []int) map[int]int {
	m := make(map[int]int)
	for i, n := range nums {
		m[n] = i
	}
	return m
}

func getTargetNums(nums []int, m map[int]int, target int) (int, int, int) {
	for i1, n1 := range nums {
		for i2 := i1+1; i2 < len(nums); i2++ {
			n2 := nums[i2]
			n3 := target - n1 - n2
			if i3, ok := m[n3]; ok && i1 != i3 && i2 != i3 {
				return n1, n2, n3
			}
		}
	}
	return 0, 0, 0
} 

func main() {
	start := time.Now()
	rawNums, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	}
	nums := convertInputToNums(rawNums)
	m := createNumMap(nums)
	n1, n2, n3 := getTargetNums(nums, m, 2020)
	fmt.Println(n1 * n2 * n3)

	duration := time.Since(start)
	fmt.Println(duration)
}