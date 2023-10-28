#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 2 ]; then
  echo "Please provide the year and day as arguments."
  exit 1
fi

year=$1
day=$2

# Create the year directory if it doesn't exist
if [ ! -d "$year" ]; then
  mkdir "$year"
fi

# Create the day directory if it doesn't exist
if [ ! -d "$year/day$day" ]; then
  mkdir "$year/day$day"
fi

# Create the solution.py file if it doesn't exist and add the specified code
if [ ! -f "$year/day$day/solution.py" ]; then
  echo "from lib.parse import parse_integers

def example() -> None:
    data = parse_integers(\"$year/day$day/input.txt\")
    return None" > "$year/day$day/solution.py"
fi

# Create the input.txt file if it doesn't exist
if [ ! -f "$year/day$day/input.txt" ]; then
  touch "$year/day$day/input.txt"
fi