use std::collections::HashMap;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A {}", part_a(INPUT));
    println!("Part B {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    run_slow(data, 10)
}

fn part_b(data: &str) -> usize {
    run(data, 40)
}

fn run(data: &str, steps: usize) -> usize {
    let (mut template, rules) = parse_data(data);

    for _ in 0..steps {
        template = insertion(template, &rules);
    }

    let mut freqs = frequency_analysis(&template)
        .iter()
        .map(|(&k, &v)| (k, v))
        .collect::<Vec<(char, usize)>>();
    freqs.sort_by(|a, b| a.1.cmp(&b.1));
    freqs.last().unwrap().1 - freqs.first().unwrap().1
}

fn parse_data(
    data: &str,
) -> (
    HashMap<TwoGram, usize>,
    HashMap<TwoGram, (TwoGram, TwoGram)>,
) {
    let split = data.split("\n\n").collect::<Vec<&str>>();
    (parse_sequence(split[0]), parse_rules(split[1]))
}

fn parse_sequence(sequence: &str) -> HashMap<TwoGram, usize> {
    let mut template = HashMap::new();

    for idx in 1..sequence.len() {
        let two_gram = TwoGram::from_string(&sequence[idx - 1..=idx]);
        let count = template.entry(two_gram).or_insert(0);
        *count += 1;
    }

    template
}

fn parse_rules(map: &str) -> HashMap<TwoGram, (TwoGram, TwoGram)> {
    map.lines()
        .map(|line| {
            let split = line.split(" -> ").collect::<Vec<&str>>();
            let key_c1 = split[0].chars().nth(0).unwrap();
            let key_c2 = split[0].chars().nth(1).unwrap();
            let val_c = split[1].chars().nth(0).unwrap();
            let key = TwoGram::new(key_c1, key_c2);
            let val1 = TwoGram::new(key_c1, val_c);
            let val2 = TwoGram::new(val_c, key_c2);

            (key, (val1, val2))
        })
        .collect()
}

fn insertion(
    template: HashMap<TwoGram, usize>,
    rules: &HashMap<TwoGram, (TwoGram, TwoGram)>,
) -> HashMap<TwoGram, usize> {
    let mut new_template = HashMap::new();

    for (tg, count) in template {
        match rules.get(&tg) {
            Some((left, right)) => {
                let left_count = new_template.entry(*left).or_insert(0);
                *left_count += count;

                let right_count = new_template.entry(*right).or_insert(0);
                *right_count += count;
            }
            None => {
                let new_count = new_template.entry(tg).or_insert(0);
                *new_count += count;
            }
        }
    }

    new_template
}

fn frequency_analysis(template: &HashMap<TwoGram, usize>) -> HashMap<char, usize> {
    let mut frequency_map = HashMap::new();

    for (k, val) in template {
        let count1 = frequency_map.entry(k.c1).or_insert(0);
        *count1 += val;
        let count2 = frequency_map.entry(k.c2).or_insert(0);
        *count2 += val;
    }

    frequency_map
        .iter()
        .map(|(&k, v)| (k, (v + 1) / 2))
        .collect()
}

fn run_slow(data: &str, steps: usize) -> usize {
    let (mut template, rules) = parse_data_slow(data);

    for _ in 0..steps {
        template = insertion_slow(template, &rules);
    }

    let mut freqs = frequency_analysis_slow(template)
        .iter()
        .map(|(&k, &v)| (k, v))
        .collect::<Vec<(char, usize)>>();
    freqs.sort_by(|a, b| a.1.cmp(&b.1));
    freqs.last().unwrap().1 - freqs.first().unwrap().1
}

fn parse_data_slow(data: &str) -> (String, HashMap<String, char>) {
    let split = data.split("\n\n").collect::<Vec<&str>>();

    (parse_sequence_slow(split[0]), parse_rules_slow(split[1]))
}

fn parse_sequence_slow(sequence: &str) -> String {
    String::from(sequence)
}

fn parse_rules_slow(map: &str) -> HashMap<String, char> {
    map.lines()
        .map(|line| {
            let split = line.split(" -> ").collect::<Vec<&str>>();
            (String::from(split[0]), split[1].chars().nth(0).unwrap())
        })
        .collect()
}

fn insertion_slow(template: String, rules: &HashMap<String, char>) -> String {
    let mut new_template = String::new();

    for idx in 1..template.len() {
        let mut from = String::from(&template[idx - 1..=idx]);

        match rules.get(&from) {
            Some(&c) => {
                from.insert(1, c);
                new_template.push_str(&from[0..=1]);
            }
            None => new_template.push_str(&from[0..1]),
        }
    }

    new_template.push_str(&template[template.len() - 1..]);

    new_template
}

fn frequency_analysis_slow(template: String) -> HashMap<char, usize> {
    let mut frequency_map = HashMap::new();

    for c in template.chars() {
        let count = frequency_map.entry(c).or_insert(0);
        *count += 1;
    }

    frequency_map
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct TwoGram {
    c1: char,
    c2: char,
}

impl TwoGram {
    fn from_string(s: &str) -> TwoGram {
        TwoGram {
            c1: s.chars().nth(0).unwrap(),
            c2: s.chars().nth(1).unwrap(),
        }
    }

    fn new(c1: char, c2: char) -> TwoGram {
        TwoGram { c1: c1, c2: c2 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 1588);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 2188189693529);
    }
}
