const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A {}", part_a(INPUT));
    println!("Part B {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    let numbers = parse_input(data);
    let number = sum(&numbers);
    magnitude(number)
}

fn part_b(data: &str) -> usize {
    let mut mag = 0;
    let numbers = parse_input(data);

    for left_idx in 0..numbers.len() {
        for right_idx in 0..numbers.len() {
            if left_idx != right_idx {
                let sum = add(&numbers[left_idx], &numbers[right_idx]);
                let new_mag = magnitude(sum);
                if new_mag > mag {
                    mag = new_mag;
                }
            }
        }
    }

    mag
}

fn parse_input(data: &str) -> Vec<Vec<SnailNumber>> {
    let mut result = Vec::new();

    for line in data.lines() {
        result.push(Vec::new());
        let len = result.len();
        let mut depth = 0;
        for c in line.chars() {
            match c {
                '[' => depth += 1,
                ']' => depth -= 1,
                '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0' => {
                    result[len - 1].push(SnailNumber {
                        depth: depth,
                        val: c.to_digit(10).unwrap() as usize,
                    })
                }
                _ => continue,
            }
        }
    }

    result
}

fn magnitude(number: Vec<SnailNumber>) -> usize {
    let mut intermediate = number;

    for depth in (1..=4).rev() {
        intermediate = collapse(&mut intermediate, depth);
    }

    intermediate[0].val
}

fn collapse(number: &Vec<SnailNumber>, depth: u8) -> Vec<SnailNumber> {
    let mut result = Vec::new();
    let mut idx = 0;
    while idx < number.len() {
        if number[idx].depth != depth {
            result.push(number[idx]);
            idx += 1;
        } else {
            result.push(SnailNumber {
                depth: depth - 1,
                val: 3 * number[idx].val + 2 * number[idx + 1].val,
            });
            idx += 2
        }
    }

    result
}

fn sum(numbers: &Vec<Vec<SnailNumber>>) -> Vec<SnailNumber> {
    numbers[1..]
        .iter()
        .fold(numbers[0].clone(), |acc, number| add(&acc, number))
}

fn add(left: &Vec<SnailNumber>, right: &Vec<SnailNumber>) -> Vec<SnailNumber> {
    let mut result = Vec::new();

    for number in left {
        result.push(SnailNumber {
            depth: number.depth + 1,
            val: number.val,
        });
    }

    for number in right {
        result.push(SnailNumber {
            depth: number.depth + 1,
            val: number.val,
        });
    }

    while reduce_one(&mut result) {}

    result
}

fn reduce_one(number: &mut Vec<SnailNumber>) -> bool {
    for idx in 0..number.len() {
        if number[idx].depth >= 5 {
            explode(number, idx);
            return true;
        }
    }

    for idx in 0..number.len() {
        if number[idx].val >= 10 {
            split(number, idx);
            return true;
        }
    }

    false
}

fn explode(number: &mut Vec<SnailNumber>, loc: usize) {
    if loc > 0 {
        // println!("{:?} {:?}", number[loc - 1], number[loc]);
        number[loc - 1].val += number[loc].val;
    }

    if loc < number.len() - 2 {
        // println!("{:?} {:?}", number[loc + 1], number[loc + 2]);
        number[loc + 2].val += number[loc + 1].val;
    }

    number[loc].depth -= 1;
    number[loc].val = 0;
    number.remove(loc + 1);
}

fn split(number: &mut Vec<SnailNumber>, loc: usize) {
    let left = number[loc].val / 2;
    let right = (number[loc].val + 1) / 2;
    let depth = number[loc].depth + 1;
    number.remove(loc);
    number.insert(
        loc,
        SnailNumber {
            depth: depth,
            val: right,
        },
    );
    number.insert(
        loc,
        SnailNumber {
            depth: depth,
            val: left,
        },
    );
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct SnailNumber {
    depth: u8,
    val: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    const EXPLODE_INPUT: &str = include_str!("explode_test.txt");
    const EXPLODE_ANSWERS: &str = include_str!("explode_answers.txt");
    const SPLIT_ANSWERS: &str = include_str!("split_answers.txt");
    const SUM_INPUT_1: &str = include_str!("sum_test1.txt");
    const SUM_INPUT_2: &str = include_str!("sum_test2.txt");
    const SUM_INPUT_3: &str = include_str!("sum_test3.txt");
    const SUM_INPUT_4: &str = include_str!("sum_test4.txt");
    const SUM_ANSWER_1: &str = include_str!("sum_answer1.txt");
    const SUM_ANSWER_2: &str = include_str!("sum_answer2.txt");
    const SUM_ANSWER_3: &str = include_str!("sum_answer3.txt");
    const SUM_ANSWER_4: &str = include_str!("sum_answer4.txt");
    const MAGNITUDE_INPUT: &str = include_str!("magnitude_test.txt");
    const PART_B_TEST: &str = include_str!("part_b_test.txt");

    // const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_explode() {
        let mut test_numbers = parse_input(EXPLODE_INPUT);
        let test_answers = parse_input(EXPLODE_ANSWERS);

        for idx in 0..test_numbers.len() {
            reduce_one(&mut test_numbers[idx]);
            assert_eq!(test_numbers[idx], test_answers[idx]);
        }
    }

    #[test]
    fn test_split() {
        let mut test_numbers = vec![
            vec![
                SnailNumber { depth: 1, val: 10 },
                SnailNumber { depth: 1, val: 0 },
            ],
            vec![
                SnailNumber { depth: 1, val: 11 },
                SnailNumber { depth: 1, val: 0 },
            ],
            vec![
                SnailNumber { depth: 1, val: 12 },
                SnailNumber { depth: 1, val: 0 },
            ],
        ];
        let test_answers = parse_input(SPLIT_ANSWERS);

        for idx in 0..test_numbers.len() {
            reduce_one(&mut test_numbers[idx]);
            assert_eq!(test_numbers[idx], test_answers[idx]);
        }
    }

    #[test]
    fn test_sum_1() {
        let test_numbers = parse_input(SUM_INPUT_1);
        let test_answers = parse_input(SUM_ANSWER_1);
        let result = sum(&test_numbers);

        assert_eq!(result, test_answers[0]);
    }

    #[test]
    fn test_sum_2() {
        let test_numbers = parse_input(SUM_INPUT_2);
        let test_answers = parse_input(SUM_ANSWER_2);
        let result = sum(&test_numbers);

        assert_eq!(result, test_answers[0]);
    }

    #[test]
    fn test_sum_3() {
        let test_numbers = parse_input(SUM_INPUT_3);
        let test_answers = parse_input(SUM_ANSWER_3);
        let result = sum(&test_numbers);

        assert_eq!(result, test_answers[0]);
    }

    #[test]
    fn test_sum_4() {
        let test_numbers = parse_input(SUM_INPUT_4);
        let test_answers = parse_input(SUM_ANSWER_4);
        let result = sum(&test_numbers);

        assert_eq!(result, test_answers[0]);
    }

    #[test]
    fn test_magnitude() {
        let test_numbers = parse_input(MAGNITUDE_INPUT);
        let answers = vec![143, 1384, 445, 791, 1137, 3488];

        for idx in 0..answers.len() {
            assert_eq!(magnitude(test_numbers[idx].clone()), answers[idx]);
        }
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(PART_B_TEST), 3993);
    }
}
