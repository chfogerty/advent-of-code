use std::collections::{HashSet, VecDeque};

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_b(data: &str) -> usize {
    let target = parse_data(data);
    get_all_velocities(target).len()
}

fn part_a(data: &str) -> isize {
    let target = parse_data(data);
    let vel = get_starting_velocity(target);
    get_peak(vel)
}

fn get_all_velocities(target: ((isize, isize), (isize, isize))) -> HashSet<(isize, isize)> {
    let mut velocities = HashSet::new();
    let max_y = abs_max(target.1 .0, target.1 .1);

    for y_vel in -1 * max_y..=max_y {
        let y_steps = calc_y_steps(y_vel, target.1);
        for y_step in &y_steps {
            for offset in 0..=target.0 .1 {
                let x_steps = (target.0 .1 - (y_step - 1) - offset..=target.0 .1 - offset)
                    .rev()
                    .map(|x| match x > 0 {
                        true => x,
                        false => 0,
                    })
                    .collect::<VecDeque<isize>>();
                let final_pos = x_steps.iter().sum();

                if target.0 .0 <= final_pos && final_pos <= target.0 .1 {
                    velocities.insert((x_steps[0], y_vel));
                }

                if final_pos < target.0 .0 {
                    break;
                }
            }
        }
    }

    velocities
}

fn calc_y_steps(start_y_vel: isize, y_target: (isize, isize)) -> Vec<isize> {
    let y_target_range = y_target.0..=y_target.1;

    let mut y_pos = 0;
    let mut y_vel = start_y_vel;
    let mut steps_taken = 0;
    let mut steps = Vec::new();

    // while we're above the target floor
    while y_pos >= y_target.0 {
        if y_target_range.contains(&y_pos) {
            steps.push(steps_taken);
        }
        y_pos += y_vel;
        y_vel -= 1;
        steps_taken += 1;
    }

    steps
}

fn abs_max(a: isize, b: isize) -> isize {
    match a.abs() > b.abs() {
        true => a.abs(),
        false => b.abs(),
    }
}

fn get_peak(start_velocity: isize) -> isize {
    (1..=start_velocity).sum()
}

fn get_starting_velocity(target: ((isize, isize), (isize, isize))) -> isize {
    for y_val in (target.1 .1.abs()..target.1 .0.abs()).rev() {
        let mut x_val = 0;
        let mut x_vel = 1;
        while x_val < target.0 .0 {
            x_val += x_vel;
            x_vel += 1;
        }

        if x_val <= target.0 .1 {
            return y_val;
        }
    }

    panic!("Not found");
}

fn parse_data(data: &str) -> ((isize, isize), (isize, isize)) {
    let split = data.trim().split(", ").collect::<Vec<&str>>();
    let x = &split[0]["target area: x=".len()..]
        .split("..")
        .map(|s| s.parse::<isize>().unwrap())
        .collect::<Vec<isize>>();
    let y = &split[1]["y=".len()..]
        .split("..")
        .map(|s| s.parse::<isize>().unwrap())
        .collect::<Vec<isize>>();

    ((x[0], x[1]), (y[0], y[1]))
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 45);
    }

    // #[test]
    // fn test() {
    //     let target = parse_data(INPUT);
    //     get_all_velocities(target);
    //     assert_eq!(1, 2);
    // }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 112);
    }
}
