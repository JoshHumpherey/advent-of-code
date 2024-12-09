package main

import (
	"advent-of-code/lib"
	"fmt"
	"strconv"
	"time"
)

func getInput(filePath string) ([]int, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return nil, err
	}
	inp := []int{}
	for _, char := range lines[0] {
		val, _ := strconv.Atoi(string(char))
		inp = append(inp, val)
	}
	return inp, nil
}

func buildDisk(input []int) ([]string, []string) {
	id := 0
	disk := []string{}
	ids := []string{}

	for idx := range input {
		if idx%2 == 0 {
			for i := 0; i < input[idx]; i++ {
				disk = append(disk, strconv.Itoa(id))
			}
			ids = append(ids, strconv.Itoa(id))
			id++
		} else {
			for i := 0; i < input[idx]; i++ {
				disk = append(disk, ".")
			}
		}
	}
	return disk, ids
}

func compactDiskNaive(disk []string) []string {
	i := 0
	j := len(disk) - 1
	for i < j && i < len(disk) && j >= 0 {
		if disk[i] != "." {
			i++
		} else if disk[j] == "." {
			j--
		} else {
			disk[i], disk[j] = disk[j], disk[i]
			i++
			j--
		}
	}
	return disk
}

func getDiskTarget(disk []string, t string) (int, int) {
	targetSize := 0
	targetIdx := 0
	for i := range disk {
		if disk[i] == t {
			if targetSize == 0 {
				targetIdx = i
			}
			targetSize++
		}
	}
	return targetIdx, targetSize
}

func indexDisk(disk []string, needed int) []int {
	currSize := 0
	currIdx := 0
	indices := []int{}
	for i, d := range disk {
		if d == "." {
			if currSize == 0 {
				currIdx = i
			}
			currSize += 1
		} else {
			if currSize >= needed {
				indices = append(indices, currIdx)
			}
			currIdx = 0
			currSize = 0
		}
	}
	return indices
}

func moveFile(disk []string, dest, size int, target string) []string {
	for i := range disk {
		if i >= dest && size > 0 {
			disk[i] = target
			size--
		} else if disk[i] == target {
			disk[i] = "."
		}
	}
	return disk
}

func calculateChecksum(disk []string) int {
	checksum := 0
	for i := range disk {
		if disk[i] != "." {
			id, _ := strconv.Atoi(disk[i])
			checksum += (id * i)
		}
	}
	return checksum
}

func getNaiveChecksum(input []int) int {
	disk, _ := buildDisk(input)
	compactedDisk := compactDiskNaive(disk)
	return calculateChecksum(compactedDisk)
}

func compactDiskDefragged(disk []string, ids []string) []string {
	for i := len(ids) - 1; i >= 1; i-- {
		tagetIdx, targetSize := getDiskTarget(disk, ids[i])
		freeSpace := indexDisk(disk, targetSize)
		if len(freeSpace) > 0 && freeSpace[0] < tagetIdx {
			disk = moveFile(disk, freeSpace[0], targetSize, ids[i])
		}
	}
	return disk
}

func getDefraggedChecksum(input []int) int {
	disk, ids := buildDisk(input)
	defraggedDisk := compactDiskDefragged(disk, ids)
	return calculateChecksum(defraggedDisk)
}

func main() {
	input, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := getNaiveChecksum(input)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := getDefraggedChecksum(input)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
