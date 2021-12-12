use std::collections::HashMap;

const INPUT: &str = include_str!("input.txt");

const START: &str = "start";
const END: &str = "end";

fn main() {
    println!("Part A {}", part_a(INPUT));
    println!("Part B {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    let graph = parse_data(data);
    get_paths(&graph, part_a_valid_cave).len()
}

fn part_b(data: &str) -> usize {
    let graph = parse_data(data);
    get_paths(&graph, part_b_valid_cave).len()
}

fn parse_data(data: &str) -> HashMap<&str, Vec<&str>> {
    let mut graph: HashMap<&str, Vec<&str>> = HashMap::new();

    for line in data.lines() {
        let caves = line.split("-").collect::<Vec<&str>>();
        for &cave in &caves {
            if !graph.contains_key(cave) {
                graph.insert(cave, Vec::new());
            }
        }

        graph.get_mut(caves[0]).unwrap().push(caves[1]);
        graph.get_mut(caves[1]).unwrap().push(caves[0]);
    }

    graph
}

fn get_paths<'a>(
    graph: &HashMap<&'a str, Vec<&'a str>>,
    valid_cave: impl Fn(&Vec<&str>, &str, u8) -> (u8, bool),
) -> Vec<Vec<&'a str>> {
    let mut stack: Vec<(u8, Vec<&str>)> = Vec::new();
    let mut result = Vec::new();

    stack.push((0, vec![START]));

    while !stack.is_empty() {
        let (dupes, path) = stack.pop().unwrap();

        let node = path[path.len() - 1];
        let connections = graph.get(node).unwrap();
        for &c in connections {
            let mut cloned = path.clone();
            let (dupe_delta, valid) = valid_cave(&path, c, dupes);
            if c == END {
                // we've reached the end
                cloned.push(c);
                result.push(cloned);
            } else if valid {
                cloned.push(c);
                stack.push((dupes + dupe_delta, cloned));
            }
        }
    }

    result
}

fn part_a_valid_cave(path: &Vec<&str>, next_cave: &str, _dupes: u8) -> (u8, bool) {
    // we can visit "big" caves (uppercase) as many times as we want, but we can only visit little caves once
    (
        0,
        !path.contains(&next_cave) || next_cave.chars().nth(0).unwrap().is_uppercase(),
    )
}

fn part_b_valid_cave(path: &Vec<&str>, next_cave: &str, dupes: u8) -> (u8, bool) {
    if next_cave == START {
        return (0, false);
    }

    if part_a_valid_cave(path, next_cave, dupes).1 {
        return (0, true);
    }

    // it's a lowercase value that exists in the path, so only valid if there are no other dupes
    (1, dupes == 0)
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = include_str!("test_input.txt");
    const TEST_INPUT2: &str = include_str!("test_input2.txt");
    const TEST_INPUT3: &str = include_str!("test_input3.txt");

    #[test]
    fn test_a1() {
        assert_eq!(part_a(TEST_INPUT), 10);
    }

    #[test]
    fn test_a2() {
        assert_eq!(part_a(TEST_INPUT2), 19);
    }

    #[test]
    fn test_a3() {
        assert_eq!(part_a(TEST_INPUT3), 226);
    }

    #[test]
    fn test_b1() {
        assert_eq!(part_b(TEST_INPUT), 36);
    }

    #[test]
    fn test_b2() {
        assert_eq!(part_b(TEST_INPUT2), 103);
    }

    #[test]
    fn test_b3() {
        assert_eq!(part_b(TEST_INPUT3), 3509);
    }
}
