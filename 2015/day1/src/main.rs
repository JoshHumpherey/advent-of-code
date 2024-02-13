use std::fs::File;
use std::io::{self, BufRead};

fn get_input(filename: &str) -> io::Result<String> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut lines = Vec::new();
    for line_result in reader.lines() {
        let line = line_result?;
        lines.push(line);
    }
    Ok(lines[0].clone())
}

fn get_floor(s: String) -> i64 {
    let mut floor = 0;
    for paren in s.chars() {
        match paren {
            '(' => floor += 1,
            _ => floor -= 1,
        }
    }
    return floor
}

fn get_basement_idx(s: String) -> i64 {
    let mut floor = 0;
    let mut res = -1;
    for i in 0..s.len() {
        let paren = s.chars().nth(i).unwrap();
        match paren {
            '(' => floor += 1,
            _ => floor -= 1,
        }
        if floor == -1 {
            res = (i+1) as i64;
            break;
        }
    }
    return res
}

fn main() {
    match get_input("src/input.txt") {
        Ok(input) => {
            println!("Part 1: {}", get_floor(input.clone()));
            println!("Part 2: {}", get_basement_idx(input.clone()));
        }
        Err(err) => {
            eprintln!("Error reading file: {}", err);
        }
    }
}
