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

fn hash_match(s: String, amt: i64) -> bool {
    let raw_hash = md5::compute(s);
    let full_hash = format!("{:x}", raw_hash);
    let mut leading_zeros = 0;
    for c in full_hash.chars() {
        if c == '0' {
            leading_zeros += 1
        } else {
            break
        }
    }
    return leading_zeros >= amt
}

fn get_lowest_hash(input: &String, amt: i64) -> i64{
    let mut res = 1;
    loop {
        let candidate = format!("{}{}", input, res);
        if hash_match(candidate, amt) {
            return res;
        } else {
            res += 1
        }
    }
}

fn main() {
    match get_input("src/input.txt") {
        Ok(input) => {
            println!("Part 1: {}", get_lowest_hash(&input, 5));
            println!("Part 2: {}", get_lowest_hash(&input, 6));
        }
        Err(err) => {
            eprintln!("Error reading file: {}", err);
        }
    }
}
