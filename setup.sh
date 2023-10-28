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

# Create the files if they don't exist
if [ ! -f "$year/day$day/solution.py" ]; then
  touch "$year/day$day/solution.py"
fi

if [ ! -f "$year/day$day/input.txt" ]; then
  touch "$year/day$day/input.txt"
fi