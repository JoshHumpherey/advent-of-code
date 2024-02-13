use std::fs::File;
use std::io::{self, BufRead};

struct Dimensions {
    length: i64,
    width: i64,
    height: i64,
}

fn get_package_dimensions(filename: &str) -> io::Result<Vec<Dimensions>> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut lines = Vec::new();
    for line_result in reader.lines() {
        let line = line_result?;
        lines.push(line);
    }

    let mut dims = Vec::new();
    for l in lines {
        let parts: Vec<&str> = l.split('x').collect();
        let d = Dimensions {
            length: parts[0].parse::<i64>().unwrap_or_default(),
            width: parts[1].parse::<i64>().unwrap_or_default(),
            height: parts[2].parse::<i64>().unwrap_or_default(),
        };
        dims.push(d)
    }

    Ok(dims)
}

fn get_needed_wrapping_paper(dimensions: &Vec<Dimensions>) -> i64 {
    let mut total = 0;
    for d in dimensions {
        let s1 = d.length * d.width;
        let s2 = d.width * d.height;
        let s3 = d.height * d.length;
        let min_side = s1.min(s2).min(s3);
        total += s1*2 + s2*2 + s3*2 + min_side
    }
    return total
}

fn get_needed_ribbon(dimensions: &Vec<Dimensions>) -> i64 {
    let mut total = 0;
    for d in dimensions {
        let mut sides = [d.length, d.width, d.height];
        sides.sort();
        let product: i64 = sides.iter().product();
        total += sides[0]*2 + sides[1]*2 + product;
    }
    return total
}

fn main() {
    match get_package_dimensions("src/input.txt") {
        Ok(dimensions) => {
            println!("Part 1: {}", get_needed_wrapping_paper(&dimensions));
            println!("Part 2: {}", get_needed_ribbon(&dimensions));
        }
        Err(err) => {
            eprintln!("Error reading file: {}", err);
        }
    }
}
