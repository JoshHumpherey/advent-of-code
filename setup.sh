#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 3 ]; then
  echo "Please provide the year, day, and language as arguments."
  exit 1
fi

year=$1
day=$2
lang=$3

# Create the year directory if it doesn't exist
if [ ! -d "$year" ]; then
  mkdir "$year"
fi

# Create the day directory if it doesn't exist
if [ ! -d "$year/day$day" ]; then
  mkdir "$year/day$day"
fi

if [ "$lang" = "python" ]; then
    # Handle local imports
    export PYTHONPATH=.

    if [ ! -f "$year/day$day/solution.py" ]; then
      echo "from lib.parse import parse_strings

def example() -> None:
    data = parse_strings(\"$year/day$day/input.txt\")
    return None
    
print(example())" > "$year/day$day/solution.py"
    fi
elif [ "$lang" = "rust" ]; then
    # Initialize w/ Cargo
    cd $year/day$day
    cargo init
    cd src/

    if [ ! -f "$year/day$day/src/main.rs" ]; then
      echo "use std::fs::File;
use std::io::{self, BufRead};


fn get_input(filename: &str) -> io::Result<Vec<String>> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut lines = Vec::new();
    for line_result in reader.lines() {
        let line = line_result?;
        lines.push(line);
    }
    Ok(lines)
}

fn part_1(input: &Vec<String>) -> String{
    return input[0].clone();
}

fn main() {
    match get_input(\"src/input.txt\") {
        Ok(input) => {
            println!(\"Part 1: {}\", part_1(&input));
        }
        Err(err) => {
            eprintln!(\"Error reading file: {}\", err);
        }
    }
}" > "main.rs"
    fi

    
elif [ "$lang" = "golang" ]; then
  if [ ! -f "$year/day$day/solution.go" ]; then
    echo "package main

  import (
    \"advent-of-code/lib\"
    \"fmt\"
    \"os\"
    \"time\"
  )

  func getInput(filePath string) ([]string, error) {
    lines, err := lib.ParseStrings(filePath)
    if err != nil {
      return nil, err
    }
    return lines, nil
  }

  func dummy(lines []string) int {
    return 0
  }

  func main() {
    lines, err := getInput(\"input.txt\")
    if err != nil {
      panic(err)
    }

    p1Start := time.Now()
    part1 := dummy(lines)
    fmt.Printf(\"Part 1: %d (%s)\n\", part1, time.Since(p1Start))
  }" > "$year/day$day/solution.go"
  fi
else
    echo "Unknown language"
    exit 1
fi


# Create the solution.py file if it doesn't exist and add the specified code
if [ ! -f "$year/day$day/$FILENAME" ]; then
  echo $CONTENTS > "$year/day$day/$FILENAME"
fi

# Create the input.txt file if it doesn't exist
if [ ! -f "$year/day$day/input.txt" ]; then
  touch "$year/day$day/input.txt"
fi