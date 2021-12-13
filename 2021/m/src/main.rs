use std::collections::{HashSet, VecDeque};

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A {}", fold_manual(INPUT));
}

fn fold_manual(data: &str) -> usize {
    let (mut points, mut folds) = parse_data(data);

    let mut result = usize::MAX;

    while !folds.is_empty() {
        let fold = folds.pop_front().unwrap();

        perform_fold(&mut points, fold);

        if result == usize::MAX {
            result = points.len();
        }
    }

    let (width, height) = determine_grid_size(&points);

    print_points(&points, width, height);

    result
}

fn parse_data(data: &str) -> (HashSet<(u32, u32)>, VecDeque<(FoldDirection, u32)>) {
    let mut points = HashSet::new();
    let mut folds = VecDeque::new();
    let mut reading_points = true;

    for line in data.lines() {
        if line == "" {
            reading_points = false;
            continue;
        }

        if reading_points {
            let coords = line
                .split(",")
                .map(|s| s.parse::<u32>().unwrap())
                .collect::<Vec<_>>();
            points.insert((coords[0], coords[1]));
        } else {
            let fold = line.split("=").collect::<Vec<_>>();
            let direction = match fold[0].chars().last().unwrap() {
                'x' => FoldDirection::Left,
                'y' => FoldDirection::Up,
                _ => FoldDirection::None,
            };
            let location = fold[1].parse::<u32>().unwrap();

            if direction != FoldDirection::None {
                folds.push_back((direction, location));
            }
        }
    }

    (points, folds)
}

fn determine_grid_size(points: &HashSet<(u32, u32)>) -> (u32, u32) {
    let mut width = 0;
    let mut height = 0;

    for point in points {
        if point.0 > width {
            width = point.0;
        }

        if point.1 > height {
            height = point.1;
        }
    }

    (width, height)
}

fn print_points(points: &HashSet<(u32, u32)>, width: u32, height: u32) {
    for y in 0..=height {
        for x in 0..=width {
            match points.contains(&(x, y)) {
                true => print!("█"),
                false => print!(" "),
            };
        }
        println!();
    }
}

fn perform_fold(points: &mut HashSet<(u32, u32)>, fold: (FoldDirection, u32)) {
    let modified_points = points
        .iter()
        .filter(|p| affected_by_fold(p, &fold))
        .map(|p| adjust_for_fold(p, &fold))
        .collect::<Vec<(u32, u32)>>();

    points.retain(|p| !affected_by_fold(p, &fold));

    for point in modified_points {
        points.insert(point);
    }
}

fn affected_by_fold(point: &(u32, u32), fold: &(FoldDirection, u32)) -> bool {
    (fold.0 == FoldDirection::Up && point.1 > fold.1)
        || (fold.0 == FoldDirection::Left && point.0 > fold.1)
}

fn adjust_for_fold(point: &(u32, u32), fold: &(FoldDirection, u32)) -> (u32, u32) {
    if fold.0 == FoldDirection::Up {
        let new_coord = fold.1 - (point.1 - fold.1);
        (point.0, new_coord)
    } else {
        let new_coord = fold.1 - (point.0 - fold.1);
        (new_coord, point.1)
    }
}

#[derive(Debug, PartialEq)]
enum FoldDirection {
    Up,
    Left,
    None,
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(fold_manual(TEST_INPUT), 17);
    }
}
