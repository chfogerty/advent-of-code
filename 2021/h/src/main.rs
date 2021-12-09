use std::{cmp::Ordering, collections::HashSet};

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("{}", part_a_solution(INPUT));
    println!("{}", part_b_solution(INPUT));
}

fn part_a_solution(data: &str) -> usize {
    data.trim()
        .lines()
        .map(DisplayData::from)
        .fold(0, |acc, display_data| {
            acc + display_data
                .output
                .iter()
                .filter(|digit| {
                    digit.len() == 2 || digit.len() == 3 || digit.len() == 4 || digit.len() == 7
                })
                .count()
        })
}

fn part_b_solution(data: &str) -> usize {
    let display_data: Vec<DisplayData> = data.trim().lines().map(DisplayData::from).collect();

    let mut sum: usize = 0;
    for mut data in display_data {
        data.input = sort_input(data.input);
        let output: Vec<HashSet<char>> = data
            .output
            .iter()
            .map(|digit| digit.chars().collect::<HashSet<char>>())
            .collect();
        sum += get_display_value(&(data.input), &output);
    }

    sum
}

fn get_display_value(input: &Vec<HashSet<char>>, output: &Vec<HashSet<char>>) -> usize {
    let mut total: usize = 0;

    for digit in output {
        total *= 10;
        for idx in 0..input.len() {
            if input[idx]
                .symmetric_difference(digit)
                .collect::<Vec<&char>>()
                .len()
                == 0
            {
                total += idx;
                break;
            }
        }
    }

    total
}

// input is pre-sorted by length
fn sort_input(input: Vec<HashSet<char>>) -> Vec<HashSet<char>> {
    let mut result: Vec<HashSet<char>> = vec![HashSet::new(); 10];
    let mut used_index: HashSet<usize> = HashSet::new();

    result[1] = input[0].clone();
    result[7] = input[1].clone();
    result[4] = input[2].clone();
    result[8] = input[9].clone();
    used_index.extend([0, 1, 2, 9].iter());

    let three_index = find_index_for_3(&input, &result[1]);
    result[3] = input[three_index].clone();
    used_index.insert(three_index);

    let nine_index = find_index_for_9(&input, &result[3]);
    result[9] = input[nine_index].clone();
    used_index.insert(nine_index);

    let six_index = find_index_for_6(&input, &result[1], &result[8]);
    result[6] = input[six_index].clone();
    used_index.insert(six_index);

    let five_index = find_index_for_5(&input, &result[6]);
    result[5] = input[five_index].clone();
    used_index.insert(five_index);

    // indicies 3, 4, and 5 are nubmers 2, 3, or 5, and we're only missing 2
    let two_index = find_last_index(3, 5, &used_index);
    result[2] = input[two_index].clone();
    used_index.insert(two_index);

    // indicies 6, 7, and 8 are numbers 0, 6, or 9, and we're only missing 0
    let zero_index = find_last_index(6, 8, &used_index);
    result[0] = input[zero_index].clone();
    used_index.insert(zero_index);

    result
}

fn find_last_index(start: usize, end: usize, used_index: &HashSet<usize>) -> usize {
    for idx in start..=end {
        if !used_index.contains(&idx) {
            return idx;
        }
    }

    println!("{:?}", used_index);
    panic!("We should  never get here");
}

fn find_index_for_3(input: &Vec<HashSet<char>>, one_seg: &HashSet<char>) -> usize {
    // indicies 3, 4, and 5 are nubmers 2, 3, or 5
    for idx in 3..=5 {
        let intersection: Vec<&char> = input[idx].intersection(one_seg).collect();
        if intersection.len() == 2 {
            return idx;
        }
    }

    println!("{:?} {:?}", input, one_seg);
    panic!("We should never get here");
}

fn find_index_for_5(input: &Vec<HashSet<char>>, six_seg: &HashSet<char>) -> usize {
    // indicies 3, 4, and 5 are nubmers 2, 3, or 5
    for idx in 3..=5 {
        let difference: Vec<&char> = six_seg.difference(&input[idx]).collect();
        if difference.len() == 1 {
            return idx;
        }
    }

    println!("{:?} {:?}", input, six_seg);
    panic!("We should never get here");
}

fn find_index_for_6(
    input: &Vec<HashSet<char>>,
    one_seg: &HashSet<char>,
    eight_seg: &HashSet<char>,
) -> usize {
    // indicies 6, 7, and 8 are numbers 0, 6, or 9
    for idx in 6..=8 {
        let difference: Vec<&char> = eight_seg.difference(&input[idx]).collect();
        if one_seg.contains(difference[0]) {
            return idx;
        }
    }

    println!("{:?} {:?} {:?}", input, one_seg, eight_seg);
    panic!("We should never get here");
}

fn find_index_for_9(input: &Vec<HashSet<char>>, three_seg: &HashSet<char>) -> usize {
    // indicies 6, 7, and 8 are numbers 0, 6, or 9
    for idx in 6..=8 {
        let intersection: Vec<&char> = input[idx].intersection(three_seg).collect();
        if intersection.len() == 5 {
            return idx;
        }
    }

    println!("{:?} {:?}", input, three_seg);
    panic!("We should never get here");
}

struct DisplayData {
    input: Vec<HashSet<char>>,
    output: Vec<String>,
}

impl From<&str> for DisplayData {
    fn from(s: &str) -> Self {
        let first_split: Vec<Vec<&str>> = s
            .trim()
            .split(" | ")
            .map(|data| data.trim().split(" ").collect::<Vec<&str>>())
            .collect();
        let mut input: Vec<HashSet<char>> = first_split[0]
            .iter()
            .map(|&data| HashSet::<char>::from_iter(data.chars()))
            .collect();
        input.sort_unstable_by(|a, b| set_length_comparison(a, b));
        let output: Vec<String> = first_split[1]
            .iter()
            .map(|&data| String::from(data))
            .collect();
        DisplayData {
            input: input,
            output: output,
        }
    }
}

fn set_length_comparison(a: &HashSet<char>, b: &HashSet<char>) -> Ordering {
    if a.len() < b.len() {
        Ordering::Less
    } else if a.len() == b.len() {
        Ordering::Equal
    } else {
        Ordering::Greater
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a_solution(TEST_INPUT), 26);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b_solution(TEST_INPUT), 61229);
    }
}
