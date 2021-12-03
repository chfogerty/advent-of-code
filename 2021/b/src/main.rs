use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input.txt").expect("[ ERROR ] Failed to open file!");
    let reader = BufReader::new(file);

    let mut pt1_horizontal = 0;
    let mut pt1_depth = 0;
    let mut pt2_horizontal = 0;
    let mut pt2_depth = 0;
    let mut aim = 0;

    for line in reader.lines() {
        let unwrapped_line = line.unwrap();
        let vec: Vec<&str> = unwrapped_line.split(" ").collect();
        let delta = vec[1].parse::<i32>().unwrap();

        match vec[0] {
            "forward" => {
                pt1_horizontal += delta;
                pt2_horizontal += delta;
                pt2_depth = pt2_depth + (aim * delta);
            }
            "up" => {
                pt1_depth -= delta;
                aim -= delta;
            }
            "down" => {
                pt1_depth += delta;
                aim += delta;
            }
            _ => println!("{}", vec[0]),
        }
    }

    println!("first solution: {}", pt1_depth * pt1_horizontal);
    println!("second solution: {}", pt2_depth * pt2_horizontal);
}
