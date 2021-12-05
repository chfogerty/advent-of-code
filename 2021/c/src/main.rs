use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input.txt").expect("[ ERROR ] Failed to open file!");
    let reader = BufReader::new(file);

    let data: Vec<String> = reader
        .lines()
        .map(|l| l.expect("could not parse line"))
        .collect();

    println!("Part 1 solution: {}", calc_power(&data));
    println!("Part 2 solution: {}", calc_life_support(&data));
}

fn calc_power(data: &Vec<String>) -> u32 {
    let mut accumulator: Vec<usize> = Vec::new();

    for line in data {
        let mut idx = 0;

        for chr in line.chars() {
            if accumulator.len() == idx {
                accumulator.push(0);
            }

            match chr {
                '1' => accumulator[idx] += 1,
                '0' => {}
                _ => println!("{}", chr),
            }

            idx += 1;
        }
    }

    let midpoint: usize = data.len() / 2;
    let mut epsilon: u32 = 0;
    let mut gamma: u32 = 0;

    for bit in accumulator.iter() {
        epsilon *= 2;
        gamma *= 2;
        if bit > &midpoint {
            gamma += 1;
        } else {
            epsilon += 1;
        }
    }

    gamma * epsilon
}

fn calc_life_support(data: &Vec<String>) -> u32 {
    let (mut oxygen, mut carbon) = filter_bits(data, 0);
    for bit in 1..data[0].len() {
        if oxygen.len() > 1 {
            oxygen = filter_bits(&oxygen, bit).0;
        }

        if carbon.len() > 1 {
            carbon = filter_bits(&carbon, bit).1;
        }
    }

    str_to_int(&oxygen[0]) * str_to_int(&carbon[0])
}

fn filter_bits(data: &Vec<String>, bit: usize) -> (Vec<String>, Vec<String>) {
    let mut filtered_zeros: Vec<String> = Vec::new();
    let mut filtered_ones: Vec<String> = Vec::new();

    for line in data {
        let chars: Vec<char> = line.chars().collect();
        if chars[bit] == '0' {
            filtered_zeros.push(line.to_string());
        } else {
            filtered_ones.push(line.to_string());
        }
    }

    if filtered_zeros.len() > filtered_ones.len() {
        (filtered_zeros, filtered_ones)
    } else {
        (filtered_ones, filtered_zeros)
    }
}

fn str_to_int(s: &String) -> u32 {
    let mut val = 0;
    for c in s.chars() {
        val *= 2;
        if c == '1' {
            val += 1;
        }
    }

    val
}
