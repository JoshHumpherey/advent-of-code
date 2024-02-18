use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};

struct Santa {
    x: i64,
    y: i64,
}

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

fn move_santa(dir: char, s: &mut Santa) {
    match dir {
        '^' => {s.y += 1},
        'v' => {s.y -= 1},
        '<' => {s.x -= 1},
        '>' => {s.x += 1},
        _ => {println!("Unknown direction: {}", dir)}
    }
}

fn get_houses(input: &String) -> i64 {
    let mut santa = Santa{x: 0, y: 0};
    let mut visited: HashMap<(i64, i64), i64> = HashMap::new();
    visited.insert((0,0), 1);

    for dir in input.chars() {
        move_santa(dir, &mut santa);
        if let Some(curr) = visited.get_mut(&(santa.x, santa.y)) {
            *curr += 1;
        } else {
            visited.insert((santa.x, santa.y), 1);
        }
    }
    return visited.len() as i64
}

fn get_robo_houses(input: &String) -> i64 {
    let mut santa = Santa{x: 0, y: 0};
    let mut robo_santa = Santa{x: 0, y: 0};
    let mut visited: HashMap<(i64, i64), i64> = HashMap::new();
    visited.insert((0,0), 2);
    let mut counter = 0;

    for dir in input.chars() {
        match counter % 2 == 0 {
            true => {
                move_santa(dir, &mut santa);
                if let Some(curr) = visited.get_mut(&(santa.x, santa.y)) {
                    *curr += 1;
                } else {
                    visited.insert((santa.x, santa.y), 1);
                }
            },
            false => {
                move_santa(dir, &mut robo_santa);
                if let Some(curr) = visited.get_mut(&(robo_santa.x, robo_santa.y)) {
                    *curr += 1;
                } else {
                    visited.insert((robo_santa.x, robo_santa.y), 1);
                }
            },
        }
        counter += 1;
    }
    return visited.len() as i64
}

fn main() {
    match get_input("src/input.txt") {
        Ok(input) => {
            println!("Part 1: {}", get_houses(&input));
            println!("Part 2: {}", get_robo_houses(&input));
        }
        Err(err) => {
            eprintln!("Error reading file: {}", err);
        }
    }
}
