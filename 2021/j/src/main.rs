const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("{}", part_a(INPUT));
    println!("{}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    data.lines()
        .map(|line| score_line(line))
        .filter(|result| !result.0)
        .fold(0, |acc, result| acc + result.1)
}

fn part_b(data: &str) -> usize {
    let mut scores: Vec<usize> = data
        .lines()
        .map(|line| score_line(line))
        .filter(|result| result.0)
        .map(|result| result.1)
        .collect();

    scores.sort();

    scores[scores.len() / 2]
}

fn score_line(s: &str) -> (bool, usize) {
    let mut stack: Vec<char> = Vec::new();

    for c in s.chars() {
        let score = match c {
            '(' | '[' | '{' | '<' => {
                stack.push(match_brace(c));
                0
            }
            ')' | ']' | '}' | '>' => {
                if stack.len() == 0 {
                    score_error(c)
                } else {
                    score_char(c, stack.pop().unwrap())
                }
            }
            _ => 0,
        };

        if score != 0 {
            return (false, score);
        }
    }

    (true, score_incomplete_str(stack))
}

fn score_char(found: char, expected: char) -> usize {
    if found == expected {
        return 0;
    }

    score_error(found)
}

fn match_brace(c: char) -> char {
    match c {
        '(' => ')',
        ')' => '(',
        '[' => ']',
        ']' => '[',
        '{' => '}',
        '}' => '{',
        '<' => '>',
        '>' => '<',
        _ => '_',
    }
}

fn score_error(c: char) -> usize {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        '>' => 25137,
        _ => 0,
    }
}

fn score_incomplete_str(stack: Vec<char>) -> usize {
    stack
        .iter()
        .rev()
        .fold(0, |acc, &c| 5 * acc + score_incomplete_char(c))
}

fn score_incomplete_char(c: char) -> usize {
    match c {
        ')' => 1,
        ']' => 2,
        '}' => 3,
        '>' => 4,
        _ => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 26397);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 288957)
    }
}
