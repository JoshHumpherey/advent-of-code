package main

import (
    "fmt"
    "io/ioutil"
	"time"
	"strings"
	"strconv"
	"regexp"
)

type passport struct {
	byr string
	iyr string
	eyr string
	hgt string
	hcl string
	ecl string
	pid string
	cid string
}

func getInput() ([]string, error) {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		 return nil, err
	}
	rawLines := strings.Split(string(content), "\n")
	var normalizedLines []string
	curr := ""
	for _, l := range rawLines {
		if l == "" && curr != "" {
			normalizedLines = append(normalizedLines, curr)
			curr = ""
		} else {
			curr = strings.Join([]string{curr, l}, " ")
		}
	}
	normalizedLines = append(normalizedLines, curr)
	return normalizedLines, nil
}



func parsePassport(data string) passport {
	m := make(map[string]string)
	blobs := strings.Split(data, " ")
	for _, blob := range blobs {
		if string(blob) == "" {
			continue
		}
		vals := strings.Split(blob, ":")
		m[vals[0]] = vals[1]
	}

	return passport{
		byr: m["byr"],
		iyr: m["iyr"],
		eyr: m["eyr"],
		hgt: m["hgt"],
		hcl: m["hcl"],
		ecl: m["ecl"],
		pid: m["pid"],
		cid: m["cid"],
	}
}

func is_alphanum(word string) bool {
    return regexp.MustCompile(`^[a-zA-Z0-9]*$`).MatchString(word)
}

func isValid(p passport) bool {
	if p.byr == "" {
		return false
	}
	birthYear, _ := strconv.Atoi(p.byr)
	if birthYear < 1920 || birthYear > 2002 {
		fmt.Println("invalid birth year:", birthYear)
		return false
	}

	if p.iyr == "" {
		return false
	}
	issueYear, _ := strconv.Atoi(p.iyr)
	if issueYear < 2010 || issueYear > 2020 {
		fmt.Println("invalid issue year:", issueYear)
		return false
	}

	if p.eyr == "" {
		return false
	}
	expYear, _ := strconv.Atoi(p.eyr)
	if expYear < 2020 || expYear > 2030 {
		fmt.Println("invalid exp year:", expYear)
		return false
	}


	if p.hgt == "" {
		return false
	} else if strings.Contains(p.hgt, "cm") {
		val, _ := strconv.Atoi(strings.TrimSuffix(p.hgt, "cm"))
		if val < 150 || val > 193 {
			fmt.Println("invalid height:", val)
			return false
		}
	} else {
		val, _ := strconv.Atoi(strings.TrimSuffix(p.hgt, "in"))
		if val < 59 || val > 76 {
			fmt.Println("invalid height:", val)
			return false
		}
	}

	if p.hcl == "" {
		return false
	} else if string(p.hcl[0]) != "#" || len(p.hcl) != 7 {
		fmt.Println("invalid hair color:", p.hcl)
		return false
	} else if !is_alphanum(string(p.hcl[1:])) {
		fmt.Println("hair color not alphanum:", p.hcl)
		return false
	}

	if p.ecl == "" {
		return false
	} else {
		eyeColors := []string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
		found := false
		for _, c := range eyeColors {
			if c == p.ecl {
				found = true
				break
			}
		}

		if !found {
			fmt.Println("invalid eye color:", p.ecl)
			return false
		}
	}

	if p.pid == "" || len(p.pid) != 9 {
		fmt.Println("invalid passport id:", p.pid)
		return false
	} else if _, err := strconv.Atoi(p.pid); err != nil {
		fmt.Println("passport id not numeric:", p.pid)
		return false
	}


	return true
}

func main() {
	start := time.Now()

	rawInput, err := getInput()
	if err != nil {
		fmt.Println(err)
		return
	} 
	var passports []passport
	for _, l := range rawInput {
		p := parsePassport(l)
		passports = append(passports, p)
	}

	valid := 0
	for _, p := range passports {
		if isValid(p) {
			valid += 1
		}
	}
	fmt.Println(valid)

	duration := time.Since(start)
	fmt.Println(duration)
}