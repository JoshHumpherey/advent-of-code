use std::fs::File;
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
    match get_input("src/input.txt") {
        Ok(input) => {
            println!("Part 1: {}", part_1(&input));
        }
        Err(err) => {
            eprintln!("Error reading file: {}", err);
        }
    }
}
