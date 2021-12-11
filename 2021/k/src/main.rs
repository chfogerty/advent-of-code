use std::collections::HashSet;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn parse_data(data: &str) -> Vec<Vec<u8>> {
    data.lines()
        .map(|line| {
            line.chars()
                .map(|c| String::from(c).parse().unwrap())
                .collect::<Vec<u8>>()
        })
        .collect::<Vec<Vec<u8>>>()
}

fn part_a(data: &str) -> usize {
    let mut grid = parse_data(data);
    simulate_grid(&mut grid, 100)
}

fn part_b(data: &str) -> usize {
    let mut step = 0;
    let mut grid = parse_data(data);
    let max_flashes = grid.len() * grid[0].len();

    loop {
        step += 1;
        let flashes = simulate_step(&mut grid);

        if flashes == max_flashes {
            break;
        }
    }

    step
}

fn simulate_grid(grid: &mut Vec<Vec<u8>>, steps: usize) -> usize {
    (0..steps).fold(0, |acc, _| acc + simulate_step(grid))
}

fn simulate_step(grid: &mut Vec<Vec<u8>>) -> usize {
    let mut initial_flash = increment_all_energy(grid);

    let flash_count = flash(&mut initial_flash, grid);

    reset_flashes(grid);

    flash_count
}

fn increment_all_energy(grid: &mut Vec<Vec<u8>>) -> Vec<(usize, usize)> {
    let mut initial_flash = Vec::new();
    for row in 0..grid.len() {
        for col in 0..grid[row].len() {
            grid[row][col] += 1;
            if grid[row][col] > 9 {
                initial_flash.push((row, col));
            }
        }
    }

    initial_flash
}

fn flash(initial_flash: &mut Vec<(usize, usize)>, grid: &mut Vec<Vec<u8>>) -> usize {
    let mut stack = Vec::new();
    let mut flash_set = HashSet::new();

    stack.append(initial_flash);

    while !stack.is_empty() {
        let point = stack.pop().unwrap();
        grid[point.0][point.1] += 1;
        if grid[point.0][point.1] > 9 && !flash_set.contains(&point) {
            flash_set.insert(point);
            let mut neighbors = get_neighbors(point, grid[point.0].len(), grid.len());
            stack.append(&mut neighbors);
        }
    }

    flash_set.len()
}

fn reset_flashes(grid: &mut Vec<Vec<u8>>) {
    for row in 0..grid.len() {
        for col in 0..grid[row].len() {
            if grid[row][col] > 9 {
                grid[row][col] = 0;
            }
        }
    }
}

fn get_neighbors(point: (usize, usize), width: usize, height: usize) -> Vec<(usize, usize)> {
    let mut result = Vec::new();
    let up = point.0 > 0;
    let down = point.0 < height - 1;
    let left = point.1 > 0;
    let right = point.1 < width - 1;

    if up {
        result.push((point.0 - 1, point.1));

        if left {
            result.push((point.0 - 1, point.1 - 1));
        }

        if right {
            result.push((point.0 - 1, point.1 + 1));
        }
    }

    if down {
        result.push((point.0 + 1, point.1));

        if left {
            result.push((point.0 + 1, point.1 - 1));
        }

        if right {
            result.push((point.0 + 1, point.1 + 1));
        }
    }

    if left {
        result.push((point.0, point.1 - 1));
    }

    if right {
        result.push((point.0, point.1 + 1));
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 1656);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 195);
    }
}
