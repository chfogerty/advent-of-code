const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_a(data: &str) -> u32 {
    let elves = parse_data(data);
    let calories = sum_calories(&elves);
    *calories.iter().max().unwrap()
}

fn part_b(data: &str) -> u32 {
    let elves = parse_data(data);
    let mut calories = sum_calories(&elves);
    calories.sort_by(|a, b| b.cmp(a));

    return calories[0] + calories[1] + calories[2];
}

fn sum_calories(elves: &Vec<Vec<u32>>) -> Vec<u32> {
    elves.iter().map(|elf| elf.iter().sum()).collect()
}

fn parse_data(data: &str) -> Vec<Vec<u32>> {
    let mut elves: Vec<Vec<u32>> = Vec::new();
    let mut elf: Vec<u32> = Vec::new();

    for line in data.lines() {
        if line == "" {
            elves.push(elf);
            elf = Vec::new();
        } else {
            let cal = line.parse::<u32>().unwrap();
            elf.push(cal);
        }
    }

    elves.push(elf);

    elves
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 24000);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 45000);
    }
}
