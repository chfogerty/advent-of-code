use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_b(data: &str) -> u32 {
    let base_grid = parse_data(data);
    let grid = generate_rotations(&base_grid);
    let repetitions = (grid.len() + 1) / 2;

    let start = Point {
        large: (0, 0),
        small: (0, 0),
        grid_size: (repetitions, repetitions),
    };

    let end = Point {
        large: (repetitions - 1, repetitions - 1),
        small: (grid[0][0].len() - 1, grid[0].len() - 1),
        grid_size: (repetitions, repetitions),
    };

    a_star(start, end, &grid)
}

fn part_a(data: &str) -> u32 {
    let base_grid = parse_data(data);
    let grid = generate_rotations(&base_grid);

    let start = Point {
        large: (0, 0),
        small: (0, 0),
        grid_size: (1, 1),
    };

    let end = Point {
        large: (0, 0),
        small: (grid[0][0].len() - 1, grid[0].len() - 1),
        grid_size: (1, 1),
    };

    a_star(start, end, &grid)
}

fn parse_data(data: &str) -> Vec<Vec<u32>> {
    data.lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).unwrap())
                .collect::<Vec<u32>>()
        })
        .collect::<Vec<Vec<u32>>>()
}

fn generate_rotations(grid: &Vec<Vec<u32>>) -> Vec<Vec<Vec<u32>>> {
    let mut rotations = Vec::new();
    rotations.push(grid.clone());

    for rot in 1..10 {
        rotations.push(
            grid.iter()
                .map(|row| {
                    row.iter()
                        .map(|val| {
                            let new_val = val + rot;
                            if new_val > 9 {
                                new_val - 9
                            } else {
                                new_val
                            }
                        })
                        .collect()
                })
                .collect(),
        );
    }

    rotations
}

// start is (large grid x, large grid y, x, y)
// end is (large grid x, large grid y, x, y)
// grid is indexed grid[rotation][y][x]
// rotation is large grid x + large grid y
fn a_star(start: Point, end: Point, grid: &Vec<Vec<Vec<u32>>>) -> u32 {
    let mut open_set: BinaryHeap<Node> = BinaryHeap::new();
    let width = grid[0][0].len();
    let height = grid[0].len();

    // start->position min-cost
    let mut min_costs: HashMap<Point, u32> = HashMap::new();
    min_costs.insert(start, 0);

    // this needs reworking.
    // start->position->end heuristic cost (min_costs(point) + h(point {(rot_x, rot_y), (x, y)}, end))
    let mut cost_guess: HashMap<Point, u32> = HashMap::new();
    cost_guess.insert(
        start,
        min_costs.get(&start).unwrap() + heuristic(start, end) as u32,
    );

    open_set.push(Node {
        loc: start,
        goal: end,
        min_cost: *min_costs.get(&start).unwrap(),
        repetitions: start.grid_size.0,
    });

    while let Some(Node {
        loc,
        goal: _,
        min_cost,
        repetitions,
    }) = open_set.pop()
    {
        if loc == end {
            return min_cost;
        }

        for neighbor in generate_neighbors(loc, width, height, repetitions, repetitions) {
            if !min_costs.contains_key(&loc) {
                min_costs.insert(loc, u32::MAX);
            }

            let potential_cost = min_costs.get(&loc).unwrap()
                + grid[neighbor.rotation()][neighbor.small.1][neighbor.small.0];

            if !min_costs.contains_key(&neighbor) {
                min_costs.insert(neighbor, u32::MAX);
            }

            if potential_cost < *min_costs.get(&neighbor).unwrap() {
                min_costs.insert(neighbor, potential_cost);
                cost_guess.insert(neighbor, potential_cost + heuristic(neighbor, end) as u32);
                let neighbor_node = Node {
                    loc: neighbor,
                    goal: end,
                    min_cost: *min_costs.get(&neighbor).unwrap(),
                    repetitions: repetitions,
                };

                open_set.push(neighbor_node);
            }
        }
    }

    panic!("Didn't find a solution");
}

fn heuristic(point: Point, goal: Point) -> usize {
    let (x, y) = point.raw_xy();
    let (goal_x, goal_y) = goal.raw_xy();
    ((goal_x as isize - x as isize).abs() + (goal_y as isize - y as isize).abs()) as usize
}

fn generate_neighbors(
    point: Point,
    width: usize,
    height: usize,
    rot_width: usize,
    rot_height: usize,
) -> Vec<Point> {
    let mut result = Vec::new();

    // x, y - 1
    if point.small.1 > 0 {
        result.push(Point {
            large: point.large,
            small: (point.small.0, point.small.1 - 1),
            grid_size: point.grid_size,
        });
    } else if point.large.1 > 0 {
        result.push(Point {
            large: (point.large.0, point.large.1 - 1),
            small: (point.small.0, height - 1),
            grid_size: point.grid_size,
        })
    }

    // x, y + 1
    if point.small.1 < height - 1 {
        result.push(Point {
            large: point.large,
            small: (point.small.0, point.small.1 + 1),
            grid_size: point.grid_size,
        });
    } else if point.large.1 < rot_height - 1 {
        result.push(Point {
            large: (point.large.0, point.large.1 + 1),
            small: (point.small.0, 0),
            grid_size: point.grid_size,
        });
    }

    // x - 1, y
    if point.small.0 > 0 {
        result.push(Point {
            large: point.large,
            small: (point.small.0 - 1, point.small.1),
            grid_size: point.grid_size,
        });
    } else if point.large.0 > 0 {
        result.push(Point {
            large: (point.large.0 - 1, point.large.1),
            small: (width - 1, point.small.1),
            grid_size: point.grid_size,
        });
    }

    // x + 1, y
    if point.small.0 < width - 1 {
        result.push(Point {
            large: point.large,
            small: (point.small.0 + 1, point.small.1),
            grid_size: point.grid_size,
        });
    } else if point.large.0 < rot_width - 1 {
        result.push(Point {
            large: (point.large.0 + 1, point.large.1),
            small: (0, point.small.1),
            grid_size: point.grid_size,
        });
    }

    result
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct Point {
    large: (usize, usize),
    small: (usize, usize),
    grid_size: (usize, usize),
}

impl Point {
    fn rotation(&self) -> usize {
        self.large.0 + self.large.1
    }

    fn raw_xy(&self) -> (usize, usize) {
        (
            self.large.0 * self.grid_size.0 + self.small.0,
            self.large.1 * self.grid_size.1 + self.small.1,
        )
    }
}

#[derive(Copy, Clone)]
struct Node {
    loc: Point,
    goal: Point,
    min_cost: u32,
    repetitions: usize,
}

impl Eq for Node {}

impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.loc == other.loc
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        let f_other = other.min_cost as usize + heuristic(other.loc, other.goal);
        let f_self = self.min_cost as usize + heuristic(self.loc, self.goal);

        f_other.cmp(&f_self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 40);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 315);
    }
}
