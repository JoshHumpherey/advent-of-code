#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 2 ]; then
  echo "Please provide the year and day as arguments."
  exit 1
fi

year=$1
day=$2
day_dir=day$day

# Create the year directory if it doesn't exist
if [ ! -d "$year" ]; then
  mkdir "$year"
fi

# Create the day directory if it doesn't exist
if [ ! -d "$year/day$day" ]; then
  cd $year
  cargo new $day_dir
  cd $day_dir
else 
  cd $year/$day_dir
  cargo init
fi

cd src/
echo "" > input.txt

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