use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input.txt").expect("[ ERROR ] Failed to open file!");
    let reader = BufReader::new(file);
    let window_size = 3;
    let mut window: Vec<i32> = Vec::with_capacity(window_size);
    let mut window_total = 0;
    let mut window_value = 0;
    let mut prev_window_value = -1;
    let mut simple_total = 0;
    let mut prev_simple_value = -1;

    for line in reader.lines() {
        let cur_value = line.unwrap().parse::<i32>().unwrap();
        window_value += cur_value;

        if window.len() == 3 {
            let out = window.remove(0);
            window_value -= out;

            if prev_window_value > -1 && window_value > prev_window_value {
                window_total += 1;
            }

            prev_window_value = window_value;
        }
        if prev_simple_value > -1 && cur_value > prev_simple_value {
            simple_total += 1;
        }

        window.push(cur_value);
        prev_simple_value = cur_value;
    }

    println!("Simple total: {}", simple_total);
    println!("Sliding total: {}", window_total);
}
