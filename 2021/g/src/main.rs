const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("part a {}", part_a_solution(INPUT));
    println!("part b {}", part_b_solution(INPUT))
}

fn part_a_solution(data: &str) -> u128 {
    let mut positions = parse_data(data);
    positions.sort();

    let target_idx = positions.len() / 2;
    let target: u128;
    if positions.len() % 2 == 0 {
        target = (positions[target_idx] + positions[target_idx - 1]) / 2;
    } else {
        target = positions[target_idx];
    }

    positions.iter().map(|pos| abs_subtract(pos, &target)).sum()
}

fn part_b_solution(data: &str) -> u128 {
    let mut positions = parse_data(data);
    positions.sort();

    let mean = positions.iter().sum::<u128>() as f64 / positions.len() as f64;

    let target = mean.floor() as u128;

    let low_mean_cost = calc_cost(&positions, &target);
    let high_mean_cost = calc_cost(&positions, &(target + 1));

    if low_mean_cost < high_mean_cost {
        low_mean_cost
    } else {
        high_mean_cost
    }
}

fn parse_data(data: &str) -> Vec<u128> {
    data.split(",").map(|pos| pos.parse().unwrap()).collect()
}

fn abs_subtract(pos: &u128, target: &u128) -> u128 {
    if pos > target {
        pos - target
    } else {
        target - pos
    }
}

fn calc_cost(crabs: &Vec<u128>, target: &u128) -> u128 {
    crabs
        .iter()
        .map(|pos| {
            let dist = abs_subtract(pos, target);
            // triangle number fuel costs
            (dist * (dist + 1)) / 2
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a_solution(TEST_INPUT), 37);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b_solution(TEST_INPUT), 168);
    }
}
