use std::collections::HashSet;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a_solution(INPUT));
    println!("Part B: {}", part_b_solution(INPUT));
}

fn part_a_solution(data: &str) -> u32 {
    let grid: Vec<Vec<u32>> = parse_data(data);

    find_lowpoints(&grid)
        .iter()
        .fold(0, |acc, point| acc + grid[point.0][point.1] + 1)
}

fn part_b_solution(data: &str) -> usize {
    let grid: Vec<Vec<u32>> = parse_data(data);
    let basins = find_basins(&grid)
        .iter()
        .map(|basin| basin.len())
        .collect::<Vec<usize>>();

    return basins[0] * basins[1] * basins[2];
}

fn parse_data(data: &str) -> Vec<Vec<u32>> {
    let mut grid: Vec<Vec<u32>> = Vec::new();

    for line in data.lines() {
        let row: Vec<u32> = line
            .chars()
            .map(|c| String::from(c).parse().unwrap())
            .collect();
        grid.push(row);
    }

    grid
}

fn generate_neighbors(row: usize, col: usize, width: usize, height: usize) -> Vec<(usize, usize)> {
    let mut result: Vec<(usize, usize)> = Vec::new();

    // row - 1, col
    if row > 0 {
        result.push((row - 1, col));
    }

    // row + 1, col
    if row < height - 1 {
        result.push((row + 1, col));
    }

    // row, col - 1
    if col > 0 {
        result.push((row, col - 1));
    }

    // row, col + 1
    if col < width - 1 {
        result.push((row, col + 1));
    }

    result
}

fn is_lowpoint(val: u32, neighbor_vals: &Vec<u32>) -> bool {
    for neighbor_val in neighbor_vals {
        if &val >= neighbor_val {
            return false;
        }
    }

    return true;
}

fn find_lowpoints(grid: &Vec<Vec<u32>>) -> Vec<(usize, usize)> {
    let mut result: Vec<(usize, usize)> = Vec::new();

    for row in 0..grid.len() {
        for col in 0..grid[row].len() {
            let neighbor_points = generate_neighbors(row, col, grid[row].len(), grid.len());
            let neighbor_vals: Vec<u32> = neighbor_points
                .iter()
                .map(|point| grid[point.0][point.1])
                .collect();
            if is_lowpoint(grid[row][col], &neighbor_vals) {
                result.push((row, col));
            }
        }
    }

    result
}

fn find_basins(grid: &Vec<Vec<u32>>) -> Vec<Vec<(usize, usize)>> {
    let mut visited = HashSet::<(usize, usize)>::new();
    let mut basins = Vec::<Vec<(usize, usize)>>::new();

    for row in 0..grid.len() {
        for col in 0..grid[row].len() {
            if !visited.contains(&(row, col)) && grid[row][col] != 9 {
                basins.push(generate_basin(row, col, grid, &mut visited));
            }
        }
    }

    basins.sort_by(|a, b| b.len().cmp(&a.len()));

    basins
}

fn generate_basin(
    row: usize,
    col: usize,
    grid: &Vec<Vec<u32>>,
    visited: &mut HashSet<(usize, usize)>,
) -> Vec<(usize, usize)> {
    let mut stack: Vec<(usize, usize)> = Vec::new();
    let mut basin: Vec<(usize, usize)> = Vec::new();

    stack.push((row, col));

    while !stack.is_empty() {
        let point = stack.pop().unwrap();
        if !visited.contains(&point) && grid[point.0][point.1] != 9 {
            visited.insert(point);
            let mut neighbors =
                generate_neighbors(point.0, point.1, grid[point.0].len(), grid.len());
            stack.append(&mut neighbors);
            basin.push(point);
        }
    }

    basin
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a_solution(TEST_INPUT), 15);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b_solution(TEST_INPUT), 1134);
    }
}
