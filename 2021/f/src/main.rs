const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("part a {}", solution2(INPUT, 80));
    println!("part b {}", solution2(INPUT, 256));
}

fn solution(data: &str, days: usize) -> usize {
    let mut fish = parse_data(data);

    for day in 1..=days {
        if day % 50 == 0 {
            println!("{}", day);
        }
        let mut fish_to_add = 0;
        for idx in 0..fish.len() {
            if fish[idx] == 0 {
                fish[idx] = 6;
                fish_to_add += 1;
            } else {
                fish[idx] -= 1;
            }
        }

        if fish_to_add > 0 {
            let mut new_fish: Vec<u8> = vec![8; fish_to_add];
            fish.append(&mut new_fish);
        }
    }

    fish.len()
}

fn solution2(data: &str, days: usize) -> usize {
    let mut binned_fish = vec![0; 9];

    // bin the fish into which day they spawn new fish (only need to keep a vec of 7)
    // aka map day -> # of fish
    parse_data(data)
        .iter()
        .for_each(|fish| binned_fish[usize::from(*fish)] += 1);

    // new fish get added to current day + 2 % 7
    for day in 0..days {
        let new_fish = binned_fish[day % 7];
        binned_fish[day % 7] += binned_fish[7];
        binned_fish[7] = binned_fish[8];
        binned_fish[8] = new_fish;
    }

    binned_fish.iter().sum()
}

fn parse_data(data: &str) -> Vec<u8> {
    data.split(",")
        .map(|timer| timer.parse().unwrap())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a1() {
        assert_eq!(solution(TEST_INPUT, 18), 26);
    }

    #[test]
    fn test_a2() {
        assert_eq!(solution(TEST_INPUT, 80), 5934);
    }

    #[test]
    fn test_b1() {
        assert_eq!(solution2(TEST_INPUT, 18), 26);
    }

    #[test]
    fn test_b2() {
        assert_eq!(solution2(TEST_INPUT, 80), 5934);
    }
}
